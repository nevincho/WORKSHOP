from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List
from .models import DashboardStateUpdate

class DashboardStateSink(ABC):
    @abstractmethod
    def apply_system(self, update: DashboardStateUpdate) -> None: ...
    @abstractmethod
    def apply_target(self, update: DashboardStateUpdate) -> None: ...
    @abstractmethod
    def apply_spatial(self, update: DashboardStateUpdate) -> None: ...
    @abstractmethod
    def emit_event(self, update: DashboardStateUpdate) -> None: ...
    @abstractmethod
    def apply_diagnostic(self, update: DashboardStateUpdate) -> None: ...
    @abstractmethod
    def apply_link(self, update: DashboardStateUpdate) -> None: ...

@dataclass
class InMemoryDashboardSink(DashboardStateSink):
    systems: Dict[int, DashboardStateUpdate] = field(default_factory=dict)
    targets: Dict[int, DashboardStateUpdate] = field(default_factory=dict)
    spatials: Dict[int, DashboardStateUpdate] = field(default_factory=dict)
    events: List[DashboardStateUpdate] = field(default_factory=list)
    diagnostics: Dict[int, DashboardStateUpdate] = field(default_factory=dict)
    links: Dict[int, DashboardStateUpdate] = field(default_factory=dict)
    link_history: List[DashboardStateUpdate] = field(default_factory=list)

    def apply_system(self, update): self.systems[update.source_id] = update
    def apply_target(self, update): self.targets[update.source_id] = update
    def apply_spatial(self, update): self.spatials[update.source_id] = update
    def emit_event(self, update): self.events.append(update)
    def apply_diagnostic(self, update): self.diagnostics[update.source_id] = update
    def apply_link(self, update):
        self.links[update.source_id] = update
        self.link_history.append(update)
