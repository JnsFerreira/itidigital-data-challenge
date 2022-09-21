from typing import List

from itidigital.data_quality.builder.base import BaseBuilder
from itidigital.data_quality.schema.event import EventSchema, SchemaField, ObjectField
from itidigital.data_quality.event.event import FieldType


# TODO: Consider change `get` methods to property
class SchemaFieldBuilder(BaseBuilder):
    def __init__(self, config: dict) -> None:
        self._raw_field = config

    def get_id(self):
        return self._raw_field.get('$id')

    def get_type(self):
        try:
            type_name = self._raw_field.get('type', '')
            return FieldType[type_name.upper()]

        except KeyError:
            return FieldType.UNKNOWN

    def get_title(self):
        return self._raw_field.get('title', '')

    def get_description(self):
        return self._raw_field.get('description', '')

    def get_examples(self):
        return self._raw_field.get('examples', [])

    def construct(self) -> object:
        kwargs = {}

        for field in SchemaField.__dataclass_fields__:
            method = getattr(self, f'get_{field}')
            kwargs[field] = method()

        return SchemaField(**kwargs)


class ObjectFieldBuilder(BaseBuilder):
    def __init__(self, config: dict) -> None:
        self._raw_object_field = config

    def get_id(self):
        return self._raw_object_field.get("$id")

    def get_type(self):
        try:
            type_name = self._raw_object_field.get('type', '')
            return FieldType[type_name.upper()]

        except KeyError:
            return FieldType.UNKNOWN

    def construct(self) -> object:
        pass


class SchemaBuilder(BaseBuilder):
    def __init__(self, config: dict) -> None:
        self._raw_schema = config

    @property
    def get_schema(self) -> str:
        return self._raw_schema.get('$schema', '')

    def get_id(self):
        return self._raw_schema.get('$id', '')

    def get_type(self) -> str:
        return self._raw_schema.get('type', '')

    def get_title(self) -> str:
        return self._raw_schema.get('title', '')

    def get_description(self) -> str:
        return self._raw_schema.get('description', '')

    def get_required(self) -> List[str]:
        return self._raw_schema.get('required', [])

    @staticmethod
    def get_field(raw_field: dict):
        builder = SchemaFieldBuilder(
            config=raw_field
        )

        return builder.construct()

    def get_properties(self):
        fields = []
        properties: dict = self._raw_schema.get('properties', {})

        if not properties:
            return fields

        for name, value in properties.items():
            field = self.get_field(raw_field=value)
            fields.append(field)

        return fields

    def construct(self) -> EventSchema:
        # TODO: review error handling
        kwargs = {}

        for field in EventSchema.__dataclass_fields__:
            method = getattr(self, f'get_{field}')
            kwargs[field] = method()

        return EventSchema(**kwargs)


def main():
    import json

    file_path = '/home/jns/Documents/repos/itidigital-data-challenge/itidigital/data_quality/schema.json'
    mode = 'r'

    with open(file_path, mode) as schema_file:
        raw_schema = json.loads(schema_file.read())

    builder = SchemaBuilder(config=raw_schema)
    schema = builder.construct()
    for req_field in schema.required:
        print(req_field)

main()