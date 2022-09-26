import boto3
from moto import mock_athena, mock_s3

import itidigital.sql.json_schema_to_hive as js_2_hive
from itidigital.sql.athena.hive.properties import (
    CreateDisposition,
    TableReference,
    SerdeFormat,
    FileFormat
)


@mock_athena
@mock_s3
def main(**kwargs):
    _S3_CLIENT = boto3.client("s3", region_name='us-east-1')
    _S3_CLIENT.create_bucket(Bucket='iti-query-results')

    _ATHENA_CLIENT = boto3.client('athena', region_name='us-east-1')

    js_2_hive._ATHENA_CLIENT = _ATHENA_CLIENT
    js_2_hive.handler(**kwargs)


if __name__ == "__main__":
    table_config = {
        "location": 's3://my-bucket/my-table/',
        "create_disposition": CreateDisposition.IF_NOT_EXISTS,
        "table_reference": TableReference(
            database='itidigital',
            table_name='foo'
        ),
        "is_external": True,
        "partition_by": ['eid'],
        "clustered_by": ['documentNumber'],
        "num_buckets": 5,
        "row_format": SerdeFormat(
            name="org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe",
            properties={
                "serialization.format": ",",
                "field.delim": ",",
                "collection.delim": "|",
                "mapkey.delim": ":",
                "escape.delim": "\\"
            }
        ),
        "stored_as": FileFormat.PARQUET,
        "table_properties": {"foo": "bar", "prop_name": "prop_value"}
    }

    main(**table_config)
