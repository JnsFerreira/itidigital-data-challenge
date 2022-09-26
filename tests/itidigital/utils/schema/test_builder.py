from typing import List

import mock
import pytest

from tests.test_data import examples

from itidigital.data_quality.event.event import FieldType
from itidigital.utils.schema.event import (
    EventSchema, SchemaField, ObjectField
)
from itidigital.utils.schema.builder import (
    SchemaBuilder, SchemaFieldBuilder, ObjectFieldBuilder,
)


class TestSchemaFieldBuilder:
    @pytest.fixture
    def schema_field_builder(self) -> SchemaFieldBuilder:
        return SchemaFieldBuilder(
            config={
                "$id": "#/properties/documentNumber",
                "type": "string",
                "title": "The documentNumber schema",
                "description": "An explanation about the purpose of this instance.",
                "examples": [
                    "42323235600"
                ]
            }
        )

    def test_construct_should_works_as_expected(
        self, schema_field_builder: SchemaFieldBuilder
    ) -> None:
        """Asserts that `construct` method works as expected"""
        expected_schema_field = SchemaField(
            id="#/properties/documentNumber",
            name="documentNumber",
            type=FieldType.STRING,
            title="The documentNumber schema",
            description="An explanation about the purpose of this instance.",
            examples=["42323235600"]
        )

        schema_field = schema_field_builder.construct()

        assert schema_field == expected_schema_field

    def test_get_id_should_works_as_expected(
        self, schema_field_builder: SchemaFieldBuilder
    ) -> None:
        """Asserts that `get_id` works as expected"""
        expected_field_id = "#/properties/documentNumber"
        field_id = schema_field_builder.get_id()

        assert field_id == expected_field_id

    def test_get_name_should_works_as_expected(
        self, schema_field_builder: SchemaFieldBuilder
    ) -> None:
        """Asserts that `get_name` works as expected"""
        expected_field_name = "documentNumber"
        field_name = schema_field_builder.get_name()

        assert field_name == expected_field_name

    def test_get_type_should_works_as_expected(
        self, schema_field_builder: SchemaFieldBuilder
    ) -> None:
        """Asserts that `get_type` works as expected"""
        expected_field_type = FieldType.STRING
        field_type = schema_field_builder.get_type()

        assert field_type == expected_field_type

    def test_get_title_should_works_as_expected(
        self, schema_field_builder: SchemaFieldBuilder
    ) -> None:
        """Asserts that `get_title` works as expected"""
        expected_field_title = "The documentNumber schema"
        field_title = schema_field_builder.get_title()

        assert field_title == expected_field_title

    def test_get_description_should_works_as_expected(
            self, schema_field_builder: SchemaFieldBuilder
    ) -> None:
        """Asserts that `get_description` works as expected"""
        expected_field_desc = "An explanation about the purpose of this instance."
        field_desc = schema_field_builder.get_description()

        assert field_desc == expected_field_desc

    def test_get_examples_should_works_as_expected(
            self, schema_field_builder: SchemaFieldBuilder
    ) -> None:
        """Asserts that `get_examples` works as expected"""
        expected_field_examples = ["42323235600"]
        field_examples = schema_field_builder.get_examples()

        assert field_examples == expected_field_examples


class TestObjectFieldBuilder:
    @pytest.fixture
    def object_field_builder(self) -> ObjectFieldBuilder:
        """Fixture for `ObjectFieldBuilder` class example"""
        return ObjectFieldBuilder(
            config={
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
                        }
                    }
                }
        )

    def test_construct_works_as_expected(
        self, object_field_builder: ObjectFieldBuilder
    ) -> None:
        """Asserts that `construct` method works as expected"""
        object_field = object_field_builder.construct()

        assert isinstance(object_field, ObjectField)

    def test_get_id_should_works_as_expected(
        self, object_field_builder: ObjectFieldBuilder
    ) -> None:
        """Asserts that `get_id` works as expected"""
        expected_field_id = "#/properties/address"
        field_id = object_field_builder.get_id()

        assert field_id == expected_field_id

    def test_get_name_should_works_as_expected(
        self, object_field_builder: ObjectFieldBuilder
    ) -> None:
        """Asserts that `get_name` works as expected"""
        expected_field_name = "address"
        field_name = object_field_builder.get_name()

        assert field_name == expected_field_name

    def test_get_type_should_works_as_expected(
        self, object_field_builder: ObjectFieldBuilder
    ) -> None:
        """Asserts that `get_type` works as expected"""
        expected_field_type = FieldType.OBJECT
        field_type = object_field_builder.get_type()

        assert field_type == expected_field_type

    def test_get_title_should_works_as_expected(
        self, object_field_builder: ObjectFieldBuilder
    ) -> None:
        """Asserts that `get_title` works as expected"""
        expected_field_title = "The address schema"
        field_title = object_field_builder.get_title()

        assert field_title == expected_field_title

    def test_get_description_should_works_as_expected(
        self, object_field_builder: ObjectFieldBuilder
    ) -> None:
        """Asserts that `get_description` works as expected"""
        expected_field_desc = "An explanation about the purpose of this instance."
        field_desc = object_field_builder.get_description()

        assert field_desc == expected_field_desc

    def test_get_required_should_works_as_expected(
        self, object_field_builder: ObjectFieldBuilder
    ) -> None:
        """Asserts that `get_required` works as expected"""
        expected_field_req = [
            "street",
            "number",
            "mailAddress"
        ]

        field_req = object_field_builder.get_required()

        assert field_req == expected_field_req

    def test_get_properties_should_works_as_expected(
        self, object_field_builder: ObjectFieldBuilder
    ) -> None:
        """Asserts that `get_properties` works as expected"""
        expected_properties = [
            SchemaField(
                id='#/properties/address/properties/street',
                name='street',
                type=FieldType.STRING,
                title='The street schema',
                description='An explanation about the purpose of this instance.',
                examples=['St. Blue'])
        ]

        field_properties = object_field_builder.get_properties()

        assert field_properties == expected_properties


class TestSchemaBuilder:
    @pytest.fixture
    def schema_builder(self) -> SchemaBuilder:
        return SchemaBuilder(
            config={
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
                    }
                }
            }
        )

    def test_construct_works_as_expected(
        self, schema_builder: SchemaBuilder
    ) -> None:
        """Asserts that `construct` method works as expected"""
        schema = schema_builder.construct()

        assert isinstance(schema, EventSchema)

    def test_get_schema_should_works_as_expected(
        self, schema_builder: ObjectFieldBuilder
    ) -> None:
        """Asserts that `get_schema` works as expected"""
        expected_schema = "http://json-schema.org/draft-07/schema"
        field_schema = schema_builder.get_schema()

        assert field_schema == expected_schema



