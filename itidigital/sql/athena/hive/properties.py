import enum
from typing import Optional
from dataclasses import dataclass

__all__ = [
    'Classification',
    'TableProperties',
    'FileFormat',
    'CreateDisposition',
    'TableReference',
    'Delimiter',
    'SerdeFormat',
    'DelimiterFormat',
]


class Delimiter(enum.Enum):
    """All possible delimiter row types"""
    DELIMITED_FIELDS_TERMINATED_BY = "DELIMITED FIELDS TERMINATED BY"
    DELIMITED_COLLECTION_ITEMS_TERMINATED_BY = "DELIMITED COLLECTION ITEMS TERMINATED BY"
    MAP_KEYS_TERMINATED_BY = "MAP KEYS TERMINATED BY"
    LINES_TERMINATED_BY = "LINES TERMINATED BY"
    NULL_DEFINED_AS = "NULL DEFINED AS"


class CreateDisposition(enum.Enum):
    """All possible creation disposition values"""
    IF_NOT_EXISTS = 'IF NOT EXISTS'
    OVERWRITE = ''


class FileFormat(enum.Enum):
    """All possible file format values"""
    SEQUENCEFILE = 'sequencefile'
    TEXTFILE = 'textfile'
    RCFILE = 'rcfile'
    ORC = 'orc'
    PARQUET = 'parquet'
    AVRO = 'avro'
    ION = 'ion'
    INPUTFORMAT = 'inputformat'
    OUTPUTFORMAT = 'outputformat'


class Classification(enum.Enum):
    """All possible classification values"""
    CSV = 'csv'
    PARQUET = 'parquet'
    ORC = 'orc'
    AVRO = 'avro'
    JSON = 'json'


@dataclass
class DelimiterFormat:
    """Delimiter row format structure"""
    delimiter: Delimiter
    char: str


@dataclass
class SerdeFormat:
    """SerDe row format data structure"""
    name: str
    properties: dict


@dataclass
class TableReference:
    """Table reference data structure"""
    table_name: str
    database: Optional[str] = None


@dataclass
class TableProperties:
    """Table properties data structure"""
    classification: Classification
    has_encrypted_data: Optional[bool] = False
