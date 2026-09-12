# LORA-03 Receiver Semantics

## Link states
`NO_DATA`: no accepted advancing packet has ever been observed for the source.
`FRESH`: age of last accepted advancing packet < `stale_after_s`.
`STALE`: age >= `stale_after_s` and < `disconnect_after_s`.
`DISCONNECTED`: age >= `disconnect_after_s`.

Thresholds are injected configuration for tests only; no production timeout is selected.

Only a packet that establishes a session or advances the current-session sequence baseline refreshes freshness. Duplicate, late/out-of-order, old-session, same-session uptime-regression, and codec-invalid packets do not refresh freshness. This prevents replay/cached traffic from keeping a stale link artificially fresh.

## Sequence ordering
For the current session, `delta=(incoming-last)&0xFFFF`.
- `delta=0`: duplicate.
- `1..32767`: forward; inferred missing count = `delta-1`.
- `32768..65535`: late/out-of-order; exact half-space is conservatively late/ambiguous.

This supports `65535 -> 0` wrap and rejects an old pre-wrap packet after the baseline has advanced past wrap.

## Sessions
The first packet establishes the current session. An unseen different session ID is a runtime/session change, increments `session_changes`, resets ordering baseline, and may begin at any sequence value because v1 does not guarantee sequence zero. A previously-seen superseded session is `OLD_SESSION` and cannot modify state or freshness.

Same-session advancing sequence with lower source uptime is `UPTIME_REGRESSION`; it does not advance sequence, semantics, or freshness and is counted as out-of-order evidence.

## Event idempotence
Packet duplicates are suppressed by sequence handling. Additionally EVENT semantic delivery is deduplicated by `(source_id, session_id, event_reference)`. A new sequence carrying the same event reference advances link/order state but does not re-fire the event. The same event reference in a new session is independently valid.

## Semantic safety
Only accepted advancing packets are delivered into the minimal latest-semantic cache. Late TARGET/SPATIAL, old-session packets, duplicates, malformed packets, and uptime regressions cannot overwrite newer semantic state. DIAGNOSTIC loss changes only inferred missing count; it does not invalidate TARGET/SPATIAL state.

## Multiple sources
State is isolated per `source_id` in a dictionary of source observations. This is minimum correct source isolation only; it does not create fleet/swarm semantics.

## Metrics
Local-only: `valid_packets`, `invalid_packets`, `duplicate_packets`, `out_of_order_packets`, `inferred_missing_packets`, `session_changes`, `current_link_state`, `last_valid_age`. These are never encoded/transmitted.
