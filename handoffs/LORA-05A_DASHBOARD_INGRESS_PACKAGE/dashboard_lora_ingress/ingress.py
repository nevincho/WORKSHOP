from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from tangra_lora_v1 import MessageType
from lora03_link import LinkObserver, PacketDisposition
from .semantic_mapper import SemanticIngressRouter
from .dashboard_sink import DashboardStateSink
from .models import DashboardStateUpdate, LinkUpdate

@dataclass(frozen=True)
class IngressResult:
    accepted: bool
    disposition: str
    source_id: Optional[int]
    update: Optional[DashboardStateUpdate] = None
    error: Optional[str] = None

class ByteIngress:
    """Bytes -> unchanged LORA-02 decode through LORA-03 -> semantic sink.

    The supplied LORA-03 observer is the only packet-order/link authority.
    `receive_monotonic_time` is injected and advanced deterministically; no sleep or wall clock.
    """
    def __init__(self, observer: LinkObserver, sink: DashboardStateSink, router: SemanticIngressRouter | None = None):
        self.observer = observer
        self.sink = sink
        self.router = router or SemanticIngressRouter()
        self._last_link_signature: dict[int, tuple] = {}

    def _advance_clock_to(self, receive_monotonic_time: float) -> None:
        now = self.observer.clock.now()
        t = float(receive_monotonic_time)
        if t < now:
            raise ValueError('receive_monotonic_time regression')
        self.observer.clock.advance(t - now)

    def _link_update(self, source_id: int) -> LinkUpdate:
        m = self.observer.metrics(source_id)
        return LinkUpdate(
            link_state=m['current_link_state'],
            last_valid_age=m['last_valid_age'],
            valid_packets=m['valid_packets'],
            invalid_packets=m['invalid_packets'],
            duplicates=m['duplicate_packets'],
            out_of_order=m['out_of_order_packets'],
            inferred_missing_packets=m['inferred_missing_packets'],
            session_changes=m['session_changes'],
        )

    @staticmethod
    def _link_signature(u: LinkUpdate) -> tuple:
        # last_valid_age changes continuously under polling; state/counters define meaningful update edges.
        return (u.link_state, u.valid_packets, u.invalid_packets, u.duplicates,
                u.out_of_order, u.inferred_missing_packets, u.session_changes)

    def _emit_link_if_changed(self, source_id: int, receive_time: float, force: bool = False) -> None:
        u = self._link_update(source_id)
        sig = self._link_signature(u)
        if force or self._last_link_signature.get(source_id) != sig:
            obs = self.observer.sources.get(source_id)
            session = None if obs is None else obs.current_session_id
            envelope = DashboardStateUpdate(
                source_id=source_id, session_id=session, message_class=None,
                receive_time=float(receive_time), transport='LORA', link=u,
            )
            self.sink.apply_link(envelope)
            self._last_link_signature[source_id] = sig

    def ingest(self, data: bytes, receive_monotonic_time: float) -> IngressResult:
        self._advance_clock_to(receive_monotonic_time)
        r = self.observer.observe_bytes(bytes(data))
        if r.source_id is not None:
            self._emit_link_if_changed(r.source_id, receive_monotonic_time)
        elif r.disposition == PacketDisposition.INVALID:
            # Invalid packet source is untrusted. Update known sources only to surface the local invalid counter;
            # no source/session/semantic state is inferred from malformed bytes.
            for sid in tuple(self.observer.sources):
                self._emit_link_if_changed(sid, receive_monotonic_time)
        if not r.delivered or r.packet is None:
            return IngressResult(False, r.disposition.value, r.source_id, error=r.error)

        update = self.router.map_packet(r.packet, receive_monotonic_time)
        mt = r.packet.message_type
        if mt == MessageType.HEARTBEAT: self.sink.apply_system(update)
        elif mt == MessageType.TARGET: self.sink.apply_target(update)
        elif mt == MessageType.SPATIAL: self.sink.apply_spatial(update)
        elif mt == MessageType.EVENT: self.sink.emit_event(update)
        elif mt == MessageType.DIAGNOSTIC: self.sink.apply_diagnostic(update)
        else: raise AssertionError('decoder delivered unsupported type')
        return IngressResult(True, r.disposition.value, r.source_id, update)

    def poll_links(self, receive_monotonic_time: float) -> None:
        """Advance deterministic local time and publish FRESH/STALE/DISCONNECTED transitions."""
        self._advance_clock_to(receive_monotonic_time)
        for sid in tuple(self.observer.sources):
            self._emit_link_if_changed(sid, receive_monotonic_time)
