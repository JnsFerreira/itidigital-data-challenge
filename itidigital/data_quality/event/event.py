import enum
from typing import List, Any
from dataclasses import dataclass

__all__ = [
    'FieldType',
    'EventField',
    'Event'
]


class FieldType(enum.Enum):
    """Enum class that represents all types on JSON schema"""
    STRING = 'string'
    INTEGER = 'integer'
    OBJECT = 'object'
    ARRAY = 'array'
    BOOLEAN = 'boolean'
    NULL = 'null'
    UNKNOWN = 'unknown'

    @classmethod
    def _missing_(cls, value):
        """A lookup function used when a value is not found"""
        return cls.UNKNOWN


class PythonTypeTranslator(enum.Enum):
    STR = FieldType.STRING
    INT = FieldType.INTEGER
    FLOAT = FieldType.INTEGER
    COMPLEX = FieldType.INTEGER
    LIST = FieldType.ARRAY
    TUPLE = FieldType.ARRAY
    RANGE = FieldType.ARRAY
    SET = FieldType.ARRAY
    DICT = FieldType.OBJECT
    BOOL = FieldType.BOOLEAN
    NONE = FieldType.NULL
    UNKNOWN = FieldType.UNKNOWN

    @classmethod
    def _missing_(cls, value):
        """A lookup function used when a value is not found"""
        return cls.UNKNOWN


@dataclass
class EventField:
    """
    Class to represent the data structure of an event field

    Args:
        name (str): field name
        value (any): field value
        type (FieldType): field data type
    """
    name: str
    value: Any
    type: FieldType


@dataclass
class Event:
    """
    Class to represent the data structure of an event

    Args:
        fields (List[EventField]): List with all fields on event
    """
    fields: List[EventField]

    @property
    def json_schema(self) -> dict:
        """
        Inferred schema from event as JSON

        Returns
            dict: Inferred schema
        """
        return self._infer_schema(
            fields=self.fields
        )

    def _infer_schema(self, fields: List[EventField]) -> dict:
        """
        Infers schema based on event fields

        Args:
            fields (List[EventField]): List with all fields on event

        Returns
            dict: Inferred schema
        """
        properties = self._get_properties(fields=fields)

        base_schema = {
            "$schema": "http://json-schema.org/draft-07/schema",
            "$id": "http://example.com/example.json",
            "type": "object",
            "title": "The root schema",
            "description": "The root schema comprises the entire JSON document.",
            "required": [
            ],
        }

        return {**base_schema, **properties}

    def _get_properties(self, fields: List[EventField]) -> dict:
        """
        Gets `properties` field from schema

        Args:
            fields (List[EventField]): List with all fields on event

        Returns:
            dict: properties extract from `fields`
        """
        properties = {}

        for field in fields:
            if field.type == FieldType.OBJECT:
                properties[field.name] = self._get_properties_for_object_fields(
                    field=field
                )

            else:
                properties[field.name] = self._get_properties_for_regular_fields(
                    field=field
                )

        return {"properties": properties}

    def _get_properties_for_object_fields(self, field: EventField) -> dict:
        """
        Get properties for object (nested) fields

        Args:
            field (EventField): object field to extract properties

        Returns:
            dict: properties for object field
        """
        object_properties = self._get_properties(
            fields=field.value
        )

        object_properties["$id"] = field.name
        object_properties["type"] = FieldType.OBJECT.value

        return object_properties

    @staticmethod
    def _get_properties_for_regular_fields(field: EventField) -> dict:
        """
        Get properties for regular fields

        Args:
            field (EventField): regular field to extract properties

        Returns:
            dict: properties for regular field
        """
        return {
            "$id": field.name,
            "type": field.type.value,
            "title": f"{field.name} field",
            "description": f"{field.name} field of type {field.type.value}",
            "examples": [field.value]
        }
