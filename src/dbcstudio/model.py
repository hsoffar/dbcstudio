from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SignalModel:
    name: str
    start: int
    length: int
    byte_order: str
    is_signed: bool
    scale: float
    offset: float
    minimum: Optional[float]
    maximum: Optional[float]
    unit: str
    receivers: list[str] = field(default_factory=list)


@dataclass
class MessageModel:
    frame_id: int
    name: str
    length: int
    senders: list[str] = field(default_factory=list)
    signals: list[SignalModel] = field(default_factory=list)


@dataclass
class DbcDocument:
    path: Optional[str] = None
    version: Optional[str] = None
    messages: list[MessageModel] = field(default_factory=list)

    def message_names(self) -> list[str]:
        return [msg.name for msg in self.messages]
