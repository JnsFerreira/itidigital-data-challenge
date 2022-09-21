import enum
from typing import List, Any
from dataclasses import dataclass

from itidigital.data_quality.schema.event import EventSchema


class FieldType(enum.Enum):
    STRING = enum.auto()
    INT = enum.auto()
    OBJECT = enum.auto()
    ARRAY = enum.auto()
    BOOLEAN = enum.auto()
    NULL = enum.auto()
    UNKNOWN = enum.auto()


@dataclass
class EventField:
    value: Any
    type: FieldType


@dataclass
class Event:
    fields: List[EventField]

    @property
    def schema(self) -> EventSchema:
        return self._infer_schema()

    def _infer_schema(self) -> EventSchema:
        return EventSchema()
