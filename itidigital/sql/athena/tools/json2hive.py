from enum import Enum
from typing import Union

from itidigital.utils.schema.event import EventSchema, ObjectField
from itidigital.sql.athena.hive.table import HiveTable


class HiveType(Enum):
    STRING = 'string'
    INTEGER = 'integer'
    OBJECT = 'struct'
    ARRAY = 'array'
    BOOLEAN = 'boolean'
    NULL = 'null'
    UNKNOWN = 'unknown'


class HiveTableCreator:
    def from_event_schema(self, event_schema: EventSchema, **hive_table_kwargs) -> HiveTable:
        if 'fields' in hive_table_kwargs:
            raise KeyError("fields should not be specified on kwargs")

        hive_schema = self._json_to_hive_type_converter(
            schema=event_schema
        )

        fields = self._map_fields(schema=hive_schema)

        return HiveTable(
            fields=fields,
            **hive_table_kwargs
        )

    @staticmethod
    def _is_nested_type(field_type: HiveType):
        nested_types = [
            HiveType.OBJECT
        ]

        return True if field_type in nested_types else False

    def _json_to_hive_type_converter(self, schema: Union[EventSchema, ObjectField]):
        for field in schema.properties:
            json_type = field.type.value
            hive_type = HiveType[json_type.upper()]

            if self._is_nested_type(hive_type):
                self._json_to_hive_type_converter(field)

            field.type = hive_type

        return schema

    def _map_fields(self, schema: EventSchema) -> dict:

        fields_mapping = {}

        for field in schema.properties:
            if self._is_nested_type(field.type):
                fields_mapping[field.name] = self._map_struct_field(field)
            else:
                fields_mapping[field.name] = self._map_regular_field(field)

        return fields_mapping

    @staticmethod
    def _map_regular_field(field):
        return {
            "type": field.type.value,
            "description": field.description
        }

    def _map_struct_field(self, field):
        return {
            "type": field.type.value,
            "description": field.description,
            "fields": self._map_fields(field)
        }
