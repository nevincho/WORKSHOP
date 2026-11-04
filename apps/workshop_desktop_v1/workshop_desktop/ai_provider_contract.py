"""Provider-neutral contract for future WORKSHOP AI execution.

No provider is enabled by importing this module.
"""
from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class ModelReply:
    provider: str
    model: str
    content: str

class TextModel(Protocol):
    def generate(self, prompt: str) -> ModelReply: ...
