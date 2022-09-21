from typing import List, Any, Union
from dataclasses import dataclass


@dataclass
class SchemaField:
    id: str
    type: str
    title: str
    description: str
    examples: List[Any]


@dataclass
class ObjectField:
    id: str
    type: str
    title: str
    description: str
    required: List[str]
    properties: List[SchemaField]


@dataclass
class EventSchema(ObjectField):
    schema: str
    properties: List[Union[SchemaField, ObjectField]]



