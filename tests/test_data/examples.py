from itidigital.sql.athena.hive.properties import *


EXAMPLE_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "required": [
        "eid",
        "documentNumber",
        "name",
        "age",
        "address"
    ],
    "properties": {
        "eid": {
            "$id": "#/properties/eid",
            "type": "string",
            "title": "The eid schema",
            "description": "An explanation about the purpose of this instance.",
            "examples": [
                "3e628a05-7a4a-4bf3-8770-084c11601a12"
            ]
        },
        "documentNumber": {
            "$id": "#/properties/documentNumber",
            "type": "string",
            "title": "The documentNumber schema",
            "description": "An explanation about the purpose of this instance.",
            "examples": [
                "42323235600"
            ]
        },
        "name": {
            "$id": "#/properties/name",
            "type": "string",
            "title": "The name schema",
            "description": "An explanation about the purpose of this instance.",
            "examples": [
                "Joseph"
            ]
        },
        "age": {
            "$id": "#/properties/age",
            "type": "integer",
            "title": "The age schema",
            "description": "An explanation about the purpose of this instance.",
            "examples": [
                32
            ]
        },
        "address": {
            "$id": "#/properties/address",
            "type": "object",
            "title": "The address schema",
            "description": "An explanation about the purpose of this instance.",
            "required": [
                "street",
                "number",
                "mailAddress"
            ],
            "properties": {
                "street": {
                    "$id": "#/properties/address/properties/street",
                    "type": "string",
                    "title": "The street schema",
                    "description": "An explanation about the purpose of this instance.",
                    "examples": [
                        "St. Blue"
                    ]
                },
                "number": {
                    "$id": "#/properties/address/properties/number",
                    "type": "integer",
                    "title": "The number schema",
                    "description": "An explanation about the purpose of this instance.",
                    "examples": [
                        3
                    ]
                },
                "mailAddress": {
                    "$id": "#/properties/address/properties/mailAddress",
                    "type": "boolean",
                    "title": "The mailAddress schema",
                    "description": "An explanation about the purpose of this instance.",
                    "examples": [
                        True
                    ]
                }
            }
        }
    }
}

EXAMPLE_EVENT = {
    "eid": "3e628a05-7a4a-4bf3-8770-084c11601a12",
    "documentNumber": "42323235600",
    "name": "Joseph",
    "age": 32,
    "address": {
        "street": "St. Blue",
        "number": 3,
        "mailAddress": True
    }
}

TABLE_CONFIG = {
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