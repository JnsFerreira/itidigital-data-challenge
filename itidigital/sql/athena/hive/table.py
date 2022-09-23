import jinja2
from typing import Union, Mapping, Tuple, Optional, List


from itidigital.sql.athena.hive.properties import *
from itidigital.sql.athena.exceptions import InvalidS3LocationError


class HiveTable:
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
    ):
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
        # TODO: Adjust templates folder
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(
                '/home/jns/Documents/repos/itidigital-data-challenge/itidigital/sql/athena/statement_templates/'
            )
        )

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
        return 'EXTERNAL TABLE' if self._is_external else 'TABLE'

    @property
    def create_disposition(self) -> str:
        return self._create_disposition.value

    @property
    def table_name(self) -> str:
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
        return ', \n\t'.join(
            [self._parse_field(field) for field in self._fields.items()]
        )

    def _parse_field(self, field: Tuple) -> str:
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
        return self._comment

    @property
    def partition_by(self) -> str:
        if self._partition_by:
            print(self._partition_by)
            return ','.join([field for field in self._partition_by])

    @property
    def clustered_by(self) -> str:
        if self._clustered_by:
            return ','.join([field for field in self._clustered_by])

    @property
    def num_buckets(self) -> int:
        if self._num_buckets:
            return self._num_buckets

    @property
    def row_format(self) -> str:
        if isinstance(self._row_format, SerdeFormat):
            properties = self._row_format.properties
            serde_name = self._row_format.name
            serde_properties = ', '.join([f'"{name}" = "{value}"' for name, value in properties.items()])

            return f"SERDE {serde_name} WITH SERDEPROPERTIES ({serde_properties})"

        elif isinstance(self._row_format, DelimiterFormat):
            delimiter = self._row_format.delimiter.value
            char = self._row_format.char

            return f"{delimiter} {char}"

        else:
            raise TypeError(
                f"Expected `SerdeFormat` or `DelimiterFormat`, but got {type(self._row_format)}"
            )

    @property
    def location(self) -> str:
        s3_location = self._location
        print(s3_location)

        if not s3_location.startswith('s3://'):
            raise InvalidS3LocationError(
                "S3 location must start with `s3://`"
            )

        if not s3_location.endswith('/'):
            raise InvalidS3LocationError(
                "S3 location must end with `/`"
            )

        return s3_location

    @property
    def stored_as(self) -> str:
        return self._stored_as.value

    @property
    def table_properties(self):
        if self._table_properties:
            return ",\n\t".join(
                [f"{name} = {value}" for name, value in self._table_properties.items()]
            )
