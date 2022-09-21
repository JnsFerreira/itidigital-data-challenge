from typing import List

from itidigital.data_quality.builder.base import BaseBuilder
from itidigital.data_quality.schema.event import EventSchema, SchemaField, ObjectField
from itidigital.data_quality.event.event import FieldType


class SchemaFieldBuilder(BaseBuilder):
    def __init__(self, config: dict) -> None:
        self._config = config

    def get_id(self) -> str:
        return self._config.get('$id')

    def get_type(self) -> FieldType:
        try:
            type_name = self._config.get('type', '')
            return FieldType[type_name.upper()]

        except KeyError:
            return FieldType.UNKNOWN

    def get_title(self) -> str:
        return self._config.get('title', '')

    def get_description(self) -> str:
        return self._config.get('description', '')

    def get_examples(self) -> List:
        return self._config.get('examples', [])

    def construct(self) -> SchemaField:
        kwargs = {}

        for field in SchemaField.__dataclass_fields__:
            method = getattr(self, f'get_{field}')
            kwargs[field] = method()

        return SchemaField(**kwargs)


class ObjectFieldBuilder(BaseBuilder):
    def __init__(self, config: dict) -> None:
        self._config = config

    def get_id(self) -> str:
        return self._config.get("$id")

    def get_type(self) -> FieldType:
        try:
            type_name = self._config.get('type', '')
            return FieldType[type_name.upper()]

        except KeyError:
            return FieldType.UNKNOWN

    def get_title(self) -> str:
        return self._config.get('title', '')

    def get_description(self) -> str:
        return self._config.get('description', '')

    def get_required(self) -> List[str]:
        return self._config.get('required', [])

    def get_properties(self) -> List[SchemaField]:
        properties = []
        raw_properties: dict = self._config.get('properties')

        if not raw_properties:
            return properties

        for name, value in raw_properties.items():
            property_type_name = value.get('type', 'unknown')
            property_type = FieldType[property_type_name.upper()]

            if property_type == FieldType.OBJECT:
                builder = ObjectFieldBuilder(config=value)

            else:
                builder = SchemaFieldBuilder(config=value)

            property = builder.construct()
            properties.append(property)

        return properties

    def construct(self) -> ObjectField:
        kwargs = {}

        for field in ObjectField.__dataclass_fields__:
            method = getattr(self, f'get_{field}')
            kwargs[field] = method()

        return ObjectField(**kwargs)


class SchemaBuilder(ObjectFieldBuilder):
    def __init__(self, config: dict) -> None:
        super().__init__(config=config)
        self._config = config

    def get_schema(self) -> str:
        return self._config.get('$schema', '')

    def construct(self) -> EventSchema:
        kwargs = {}

        for field in EventSchema.__dataclass_fields__:
            method = getattr(self, f'get_{field}')
            kwargs[field] = method()

        return EventSchema(**kwargs)
