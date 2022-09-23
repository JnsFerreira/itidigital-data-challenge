from enum import Enum
from typing import Union

from itidigital.sql.athena.hive.table import HiveTable
from itidigital.utils.schema.event import EventSchema, ObjectField, SchemaField


class HiveType(Enum):
    """All possible hive types values"""
    STRING = 'string'
    INTEGER = 'integer'
    OBJECT = 'struct'
    ARRAY = 'array'
    BOOLEAN = 'boolean'
    NULL = 'null'
    UNKNOWN = 'unknown'


class HiveTableCreator:
    """
    Hive table creator class
    """
    def from_event_schema(self, event_schema: EventSchema, **hive_table_kwargs) -> HiveTable:
        """
        Creates a HiveTable class instance from a given EventSchema

        Args:
            event_schema (EventSchema): schema to infer name and types
            hive_table_kwargs (dict): Extra named arguments to be passed to `HiveTable` constructor

        Returns:
            HiveTable: class instance of `HiveTable` built based on give schema
        """
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
    def _is_nested_type(field_type: HiveType) -> bool:
        """
        Checks if whether hive type is a nested or not

        Args:
            field_type (HiveType): Hive type to be checked

        Returns:
            bool: True if is a nested type. Otherwise, False
        """
        nested_types = [
            HiveType.OBJECT
        ]

        return True if field_type in nested_types else False

    def _json_to_hive_type_converter(self, schema: Union[EventSchema, ObjectField]):
        """
        Converts schema properties from JSON types to Hive types

        Args:
            schema (Union[EventSchema, ObjectField]): schema to convert properties
        """
        for field in schema.properties:
            json_type = field.type.value
            hive_type = HiveType[json_type.upper()]

            if self._is_nested_type(hive_type):
                self._json_to_hive_type_converter(field)

            field.type = hive_type

        return schema

    def _map_fields(self, schema: EventSchema) -> dict:
        """
        Map each schema properties to a mapping object, like:

        ```
        "field_name" : {
            "type": "string",
            "description": "my field description"
        }

        Args:
            schema (EventSchema): schema to retrieve properties

        Returns:
            dict: mapping of schema properties
        """
        fields_mapping = {}

        for field in schema.properties:
            if self._is_nested_type(field.type):
                fields_mapping[field.name] = self._map_struct_field(field)
            else:
                fields_mapping[field.name] = self._map_regular_field(field)

        return fields_mapping

    @staticmethod
    def _map_regular_field(field: SchemaField) -> dict:
        """
        Converts a regular schema field to a mapping

        Args:
            field (SchemaField): schema field to be mapped
        Returns:
            dict:  mapping of schema field
        """
        return {
            "type": field.type.value,
            "description": field.description
        }

    def _map_struct_field(self, field: ObjectField) -> dict:
        """
        Converts an object schema field to a mapping

        Args:
            field (ObjectField): schema field to be mapped
        Returns:
            dict:  mapping of schema field
        """
        return {
            "type": field.type.value,
            "description": field.description,
            "fields": self._map_fields(field)
        }
