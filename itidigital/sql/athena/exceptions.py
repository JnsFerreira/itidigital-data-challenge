class InvalidS3LocationError(Exception):
    """Exception for invalid S3 locations"""
    def __init__(self, message: str) -> None:
        super().__init__(message)


class InvalidRowFormatError(Exception):
    """Exception for invalid row formats"""
    def __init__(self, message: str) -> None:
        super().__init__(message)
