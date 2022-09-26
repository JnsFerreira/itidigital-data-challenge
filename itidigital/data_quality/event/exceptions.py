"""Module for custom exceptions related events"""


class InvalidSchemaObject(TypeError):
    """Exception for invalid schema object"""
    def __init__(self, message: str) -> None:
        super().__init__(message)
