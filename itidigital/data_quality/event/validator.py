from itidigital.data_quality.schema.event import EventSchema
from itidigital.data_quality.event.event import Event


class EventValidator:
    schema: EventSchema

    def validate(self, event: Event):
        ...

    def _validate_field_type(self):
        ...

    def _validate_required_field(self):
        ...
    
    