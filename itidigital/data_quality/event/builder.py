from itidigital.data_quality.builder.base import BaseBuilder
from itidigital.data_quality.event.event import Event


class EventBuilder(BaseBuilder):
    def __init__(self, raw_event: dict) -> None:
        self._raw_event = raw_event

    def construct(self) -> Event:
        ...
    