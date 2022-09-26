from typing import List, Any, Union
from dataclasses import dataclass, field


@dataclass
class SchemaField:
    """
    Class to represent the data structure of a schema field

    Args:
        id (str): Schema field id
        name (str): Schema field name
        type (str): Schema field type
        title (str): Schema field type
        description (str): Schema field description
        examples (List[Any]): Examples of possible values
    """
    id: str = field(compare=False)
    name: str = field(compare=True)
    type: str = field(compare=True)
    title: str = field(compare=False)
    description: str = field(compare=False)
    examples: List[Any] = field(compare=False)


@dataclass
class ObjectField:
    """
    Class to represent the data structure of an object field

    Args:
        id (str): Object field id
        name (str): Object field name
        type (str): Object field type
        title (str): Object field type
        description (str): Object field description
        required (List[str]): Object field required fields
        properties (List[SchemaField]): List with all object properties
    """
    id: str = field(compare=False)
    name: str = field(compare=True)
    type: str = field(compare=True)
    title: str = field(compare=False)
    description: str = field(compare=False)
    required: List[str] = field(compare=False)
    properties: List[SchemaField] = field(compare=True)


@dataclass
class EventSchema(ObjectField):
    """
    Class to represent the data structure of an event schema

    Args:
        schema (str): schema name
        properties (List[Union[SchemaField, ObjectField]]): List with all schema properties
    """
    schema: str = field(compare=False)
    properties: List[Union[SchemaField, ObjectField]] = field(compare=True)



