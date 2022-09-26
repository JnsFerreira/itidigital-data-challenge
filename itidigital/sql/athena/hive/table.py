import os
import jinja2
from typing import Union, Mapping, Tuple, Optional, List

from itidigital.variables import PROJECT_ROOT_PATH
from itidigital.sql.athena.exceptions import InvalidS3LocationError, InvalidRowFormatError
from itidigital.sql.athena.hive.properties import (
    CreateDisposition, TableReference, FileFormat, SerdeFormat, DelimiterFormat
)


class HiveTable:
    """Represents a hive table and it's properties"""
    _TEMPLATE_PATH = os.path.join(
        PROJECT_ROOT_PATH,
        'itidigital/sql/athena/statement_templates'
    )

    def __init__(
            self,
            create_disposition: CreateDisposition,
            table_reference: TableReference,
            fields: Mapping,
            is_external: bool,
            location: str,
            stored_as: FileFormat = FileFormat.TEXTFILE,
            comment: Optional[str] = None,
            partition_by: Optional[List[str]] = None,
            clustered_by: Optional[List[str]] = None,
            num_buckets: int = None,
            row_format: Union[SerdeFormat, DelimiterFormat] = None,
            table_properties: dict = None
    ) -> None:
        """
        Initializes `HiveTable` class

        Args:
            create_disposition (CreateDisposition): Causes the error message to be suppressed if a table named
                table_name already exists.

            table_reference (TableReference): Causes the error message to be suppressed if a table named
                table_name already exists.

            fields (Mapping): Specifies the name for each column to be created, along with the column's data type

            is_external (bool): Specifies that the table is based on an underlying data file that exists in Amazon S3 or
                is managed by Athena

            location (str): Specifies the location of the underlying data in Amazon S3 from which the table is created

            stored_as (FileFormat): Specifies the file format for table data. If omitted, TEXTFILE is the default

            comment (Optional[str]): Creates the comment table property and populates it with the comment you specify.

            partition_by (Optional[List[str]]): Creates a partitioned table with one or more partition columns

            clustered_by (Optional[List[str]]): Divides, with or without partitioning, the data in the specified
                col_name columns into data subsets called buckets.

            num_buckets (int): The num_buckets parameter specifies the number of buckets to create

            row_format (Union[SerdeFormat, DelimiterFormat]): Specifies the row format of the table and its underlying
                source data if applicable

            table_properties (dict): Specifies custom metadata key-value pairs for the table definition in addition to
                predefined table properties, such as "comment".
        """
        self._create_disposition = create_disposition
        self._table_reference = table_reference
        self._fields = fields
        self._comment = comment
        self._is_external = is_external
        self._partition_by = partition_by
        self._clustered_by = clustered_by
        self._num_buckets = num_buckets
        self._row_format = row_format
        self._location = location
        self._stored_as = stored_as
        self._table_properties = table_properties

    @property
    def ddl_statement(self) -> str:
        """
        Generates a DDL statement for hive table

        Returns:
            str: DDL statement
        """
        loader = jinja2.FileSystemLoader(searchpath=self._TEMPLATE_PATH)
        env = jinja2.Environment(loader=loader)
        template = env.get_template(name='ddl.txt')

        return template.render(
            table_type=self.table_type,
            creation_disposition=self.create_disposition,
            table_name=self.table_name,
            fields=self.fields,
            comment=self.comment,
            partition_by=self.partition_by,
            clustered_by=self.clustered_by,
            num_buckets=self.num_buckets,
            row_format=self.row_format,
            stored_as=self.stored_as,
            location=self.location,
            table_properties=self.table_properties
        )

    @property
    def table_type(self):
        """Hive table type property"""
        return 'EXTERNAL TABLE' if self._is_external else 'TABLE'

    @property
    def create_disposition(self) -> str:
        """Hive table creation disposition property"""
        return self._create_disposition.value

    @property
    def table_name(self) -> str:
        """Hive table type property"""
        table = self._table_reference.table_name
        db = self._table_reference.database

        if table.startswith('_'):
            return f"`{table}`" if not db else f"`{db}.{table}`"

        elif any(i.isdigit() for i in table):
            return f'"{table}"' if not db else f'"{db}.{table}"'

        else:
            return f'{table}' if not db else f'{db}.{table}'

    @property
    def fields(self) -> str:
        """Hive table fields property"""
        return ', \n\t'.join(
            [self._parse_field(field) for field in self._fields.items()]
        )

    def _parse_field(self, field: Tuple[str, dict]) -> str:
        """
        Helper function to parse fields

        Args:
            field (Tuple): Name and attributes from a field

        Returns
            str: field formatted as string
        """
        name, attr = field
        field_type = attr.get('type')

        if 'fields' in attr:
            nested_fields = attr.get('fields', {})
            nested_structure = f"""<{', '.join(
                [self._parse_field(field).replace(' ', ':') for field in nested_fields.items()]
            )}>"""

            return f"{name} {field_type}{nested_structure}"

        return f"{name} {field_type}"

    @property
    def comment(self) -> str:
        """Hive table comment property"""
        return self._comment

    @property
    def partition_by(self) -> str:
        """Hive table partition property"""
        if self._partition_by:
            return ','.join([field for field in self._partition_by])

    @property
    def clustered_by(self) -> str:
        """Hive table clustering property"""
        if self._clustered_by:
            return ','.join([field for field in self._clustered_by])

    @property
    def num_buckets(self) -> int:
        """Hive table buckets property"""
        if self._num_buckets:
            return self._num_buckets

    @property
    def row_format(self) -> str:
        """Hive table row format property"""
        if isinstance(self._row_format, SerdeFormat):
            properties = self._row_format.properties
            serde_name = self._row_format.name
            serde_properties = ', '.join([f'"{name}" = "{value}"' for name, value in properties.items()])

            return f"SERDE {serde_name} WITH SERDEPROPERTIES ({serde_properties})"

        elif isinstance(self._row_format, DelimiterFormat):
            delimiter = self._row_format.delimiter.value
            char = self._row_format.char

            return f"{delimiter} {char}"

    @row_format.setter
    def row_format(self, value):
        if not isinstance(value, SerdeFormat) or \
                isinstance(value, DelimiterFormat):
            raise InvalidRowFormatError(
                f"Expected `SerdeFormat` or `DelimiterFormat`, but got {type(self._row_format)}"
            )

    @property
    def location(self) -> str:
        """Hive table location property"""
        return self._location

    @location.setter
    def location(self, value: str) -> str:
        if not value.startswith('s3://'):
            raise InvalidS3LocationError(
                "S3 location must start with `s3://`"
            )

        if not value.endswith('/'):
            raise InvalidS3LocationError(
                "S3 location must end with `/`"
            )

    @property
    def stored_as(self) -> str:
        """Hive table stored format property"""
        return self._stored_as.value

    @property
    def table_properties(self):
        """Hive table properties"""
        if self._table_properties:
            return ",\n\t".join(
                [f"{name} = {value}" for name, value in self._table_properties.items()]
            )
