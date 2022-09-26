from itidigital.data_quality.event.event import Event
from itidigital.utils.schema.event import EventSchema
from itidigital.utils.schema.builder import SchemaBuilder
from itidigital.data_quality.event.exceptions import InvalidSchemaObject


class EventValidator:
    """
    Event validator class
    """
    def __init__(self, schema: EventSchema):
        """
        Initializes `EventValidator` class

        Args:
            schema (EventSchema): schema to be used as reference to validate events
        """
        self._schema = schema

    @property
    def schema(self) -> EventSchema:
        """Schema property"""
        return self._schema

    @schema.setter
    def schema(self, new_schema: EventSchema) -> None:
        """
        Setter method for schema property

        Args:
            new_schema (EventSchema): new schema to be set as reference schema

        Returns
            None
        """
        if not isinstance(new_schema, EventSchema):
            raise InvalidSchemaObject(
                f"Schema should be of type EventSchema, but got {type(new_schema)}"
            )

        self._schema = new_schema

    def is_valid(self, event: Event) -> bool:
        """
        Validates if a given event conforms to a defined schema

        Args:
            event (Event): event to be checked

        Returns:
            bool: True if event schema matches the defined schema. Otherwise, False
        """
        event_schema = SchemaBuilder(
            config=event.json_schema
        ).construct()

        return event_schema == self._schema
