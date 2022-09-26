import os
import pathlib

from itidigital import variables
from itidigital.utils.schema import helpers
from itidigital.utils.schema.builder import SchemaBuilder
from itidigital.sql.athena.tools.hive_table_creator import HiveTableCreator

_ATHENA_CLIENT = None
_SCHEMA_FILE_PATH = os.path.join(
        variables.PROJECT_ROOT_PATH,
        'itidigital/sql/schema.json'
)


def create_hive_table_with_athena(query):
    """
    Creates hive table on Athena based on given DDL query
    """
    print(f"DDL Query: {query}")
    _ATHENA_CLIENT.start_query_execution(
        QueryString=query,
        ResultConfiguration={
            'OutputLocation': f's3://iti-query-results/'
        }
    )


def handler(**hive_table_kwargs) -> None:
    """
    Handles hive table creation from json schema
    """
    json_schema = helpers.load_schema(_SCHEMA_FILE_PATH)
    event_schema = SchemaBuilder(json_schema).construct()

    creator = HiveTableCreator()
    hive_table = creator.from_event_schema(
        event_schema=event_schema,
        **hive_table_kwargs
    )

    create_hive_table_with_athena(
        query=hive_table.ddl_statement
    )
