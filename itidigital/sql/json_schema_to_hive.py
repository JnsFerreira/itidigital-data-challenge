from itidigital.utils.schema import helpers
from itidigital.utils.schema.builder import SchemaBuilder
from itidigital.sql.athena.tools.json2hive import HiveTableCreator
from itidigital.sql.athena.hive.properties import (
    CreateDisposition,
    TableReference,
    SerdeFormat,
    FileFormat
)


_ATHENA_CLIENT = None
_SCHEMA_FILE_PATH = 'schema.json'


def create_hive_table_with_athena(query):
    """
    """
    print(f"Query: {query}")
    _ATHENA_CLIENT.start_query_execution(
        QueryString=query,
        ResultConfiguration={
            'OutputLocation': f's3://iti-query-results/'
        }
    )


def handler():
    """"""
    json_schema = helpers.load_schema(_SCHEMA_FILE_PATH)
    event_schema = SchemaBuilder(json_schema).construct()

    creator = HiveTableCreator()
    # TODO: adjust extra params
    hive_table = creator.from_event_schema(
        event_schema=event_schema,
        location='s3://my-bucket/my-table/',
        create_disposition=CreateDisposition.IF_NOT_EXISTS,
        table_reference=TableReference(
            database='itidigital',
            table_name='foo'
        ),
        is_external=True,
        partition_by=['eid'],
        clustered_by=['documentNumber'],
        num_buckets=5,
        row_format=SerdeFormat(
            name="org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe",
            properties={
                "serialization.format": ",",
                "field.delim": ",",
                "collection.delim": "|",
                "mapkey.delim": ":",
                "escape.delim": "\\"
            }
        ),
        stored_as=FileFormat.PARQUET,
        table_properties={"foo": "bar", "prop_name": "prop_value"}
    )

    create_hive_table_with_athena(
        query=hive_table.ddl_statement
    )
