"""Module to implement all concrete builder classes related to schema"""

from typing import List

from itidigital.data_quality.event.event import FieldType
from itidigital.utils.builder.base import BaseBuilder
from itidigital.utils.schema.event import EventSchema, SchemaField, ObjectField


class SchemaFieldBuilder(BaseBuilder):
    """Builder concrete class for `SchemaFieldBuilder`"""

    def __init__(self, config: dict) -> None:
        """
        Initializes `SchemaFieldBuilder` class

        Args:
            config (dict): SchemaField attributes as dictionary.

        Returns:
            None
        """
        self._config = config

    def construct(self) -> SchemaField:
        """
        Constructs a `SchemaField` class instance

        Returns:
            SchemaField: a class instance of SchemaField based on given configuration
        """
        kwargs = {}

        for field in SchemaField.__dataclass_fields__:
            method = getattr(self, f'get_{field}')
            kwargs[field] = method()

        return SchemaField(**kwargs)

    def get_id(self) -> str:
        """
        Gets schema field id attribute

        Returns:
            str: schema field id attribute
        """
        return self._config.get('$id', '')

    def get_name(self) -> str:
        """
        Gets schema field name attribute

        Returns:
            str: schema field name attribute
        """
        identifier = self.get_id()

        return identifier.split('/')[-1]

    def get_type(self) -> FieldType:
        """
        Gets schema field type attribute

        Returns:
            FieldType: schema field type attribute
        """
        try:
            type_name = self._config.get('type', '')
            return FieldType[type_name.upper()]

        except KeyError:
            return FieldType.UNKNOWN

    def get_title(self) -> str:
        """
        Gets schema field title attribute

        Returns:
            str: schema field title attribute
        """
        return self._config.get('title', '')

    def get_description(self) -> str:
        """
        Gets schema field description attribute

        Returns:
            str: schema field description attribute
        """
        return self._config.get('description', '')

    def get_examples(self) -> List:
        """
        Gets schema field examples attribute

        Returns:
            List: schema field examples attribute
        """
        return self._config.get('examples', [])


class ObjectFieldBuilder(BaseBuilder):
    """Builder concrete class for `SchemaFieldBuilder`"""
    def __init__(self, config: dict) -> None:
        """
        Initializes `ObjectFieldBuilder` class

        Args:
            config (dict): ObjectField attributes as dictionary.

        Returns:
            None
        """
        self._config = config

    def construct(self) -> ObjectField:
        """
        Constructs a `ObjectField` class instance

        Returns:
            ObjectField: a class instance of ObjectField based on given configuration
        """
        kwargs = {}

        for field in ObjectField.__dataclass_fields__:
            method = getattr(self, f'get_{field}')
            kwargs[field] = method()

        return ObjectField(**kwargs)

    def get_id(self) -> str:
        """
        Gets object field id attribute

        Returns:
            str: object field id attribute
        """
        return self._config.get("$id", "")

    def get_name(self) -> str:
        """
        Gets object field name attribute

        Returns:
            str: object field name attribute
        """
        identifier = self.get_id()

        return identifier.split('/')[-1]

    def get_type(self) -> FieldType:
        """
        Gets object field type attribute

        Returns:
            FieldType: object field type attribute
        """
        try:
            type_name = self._config.get('type', '')

            return FieldType[type_name.upper()]

        except KeyError:
            return FieldType.UNKNOWN

    def get_title(self) -> str:
        """
        Gets object field title attribute

        Returns:
            str: object field title attribute
        """
        return self._config.get('title', '')

    def get_description(self) -> str:
        """
        Gets object field description attribute

        Returns:
            str: object field description attribute
        """
        return self._config.get('description', '')

    def get_required(self) -> List[str]:
        """
        Gets object field required attribute

        Returns:
            List: object field required attribute
        """
        return self._config.get('required', [])

    def get_properties(self) -> List[SchemaField]:
        """
        Gets object field properties attribute

        Returns:
            List[SchemaField]: object field properties attribute
        """
        properties = []
        raw_properties: dict = self._config.get('properties', {})

        if not raw_properties:
            return properties

        for name, value in raw_properties.items():
            property_type_name = value.get('type', '')
            property_type = FieldType[property_type_name.upper()]

            if property_type == FieldType.OBJECT:
                builder = ObjectFieldBuilder(config=value)

            else:
                builder = SchemaFieldBuilder(config=value)

            property = builder.construct()
            properties.append(property)

        return properties


class SchemaBuilder(ObjectFieldBuilder):
    """Builder concrete class for `SchemaBuilder`"""

    def __init__(self, config: dict) -> None:
        """
        Initializes `SchemaBuilder` class

        Args:
            config (dict): Schema attributes as dictionary.

        Returns:
            None
        """
        super().__init__(config=config)
        self._config = config

    def construct(self) -> EventSchema:
        """
        Constructs a `EventSchema` class instance

        Returns:
            EventSchema: a class instance of EventSchema based on given configuration
        """
        kwargs = {}

        for field in EventSchema.__dataclass_fields__:
            method = getattr(self, f'get_{field}')
            kwargs[field] = method()

        return EventSchema(**kwargs)

    def get_schema(self) -> str:
        """
        Gets schema attribute

        Returns:
            str: schema attribute
        """
        return self._config.get('$schema', '')
