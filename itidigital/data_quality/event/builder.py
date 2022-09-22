"""Module to implement all concrete builder classes related to event"""

from typing import Any, List

from itidigital.data_quality.builder.base import BaseBuilder
from itidigital.data_quality.event.event import (
    Event,
    EventField,
    FieldType,
    PythonTypeTranslator
)


class EventFieldBuilder(BaseBuilder):
    """Builder concrete class for `EventBuilder`"""

    def __init__(self, config: dict) -> None:
        """
        Initializes `EventFieldBuilder` class

        Args:
            config (dict): EventField attributes as dictionary.

        Returns:
            None
        """
        self._config = config

    def construct(self) -> EventField:
        """
        Constructs a `EventField` class instance

        Returns:
            EventField: a class instance of EventField based on given configuration
        """
        kwargs = {}

        for field in EventField.__dataclass_fields__:
            method = getattr(self, f'get_{field}')
            kwargs[field] = method()

        return EventField(**kwargs)

    def get_name(self) -> str:
        """
        Gets event field name attribute

        Returns:
            str: event field name attribute
        """
        return self._config.get('name')

    def get_type(self) -> FieldType:
        """
        Gets event field type attribute

        Returns:
            str: event field type attribute
        """
        field_value = self._config.get('value')
        
        python_type = type(field_value).__name__.upper()

        return PythonTypeTranslator[python_type].value

    def get_value(self) -> Any:
        """
        Gets event field value attribute

        Returns:
            str: event field value attribute
        """
        field_type = self.get_type()

        if field_type == FieldType.OBJECT:
            field_value = self._get_value_for_object_fields()

        else:
            field_value = self._config.get('value')

        return field_value

    def _get_value_for_object_fields(self) -> List:
        """
        Gets value for nested object fields

        Returns:
            List: all nested field values on object field
        """
        values = []

        field_value = self._config.get('value')
        for name, value in field_value.items():
            config = {
                "name": name,
                "value": value
            }
            event_field = EventFieldBuilder(config).construct()
            values.append(event_field)

        return values


class EventBuilder(BaseBuilder):
    """
    Builder concrete class for `EventBuilder`
    """

    def __init__(self, config: dict) -> None:
        """
        Initializes `EventBuilder` class

        Args:
            config (dict): Event attributes as dictionary.
        """
        self._config = config

    def construct(self) -> Event:
        """
        Constructs a `Event` class instance

        Returns:
            EventField: a class instance of Event based on given configuration
        """
        kwargs = {}

        for field in Event.__dataclass_fields__:
            method = getattr(self, f'get_{field}')
            kwargs[field] = method()

        return Event(**kwargs)

    def get_fields(self) -> List:
        """
        Gets all event fields

        Returns:
            List: all fields on event
        """
        fields = []

        for name, value in self._config.items():
            config = {
                "name": name,
                "value": value
            }

            builder = EventFieldBuilder(config=config)

            fields.append(builder.construct())

        return fields

