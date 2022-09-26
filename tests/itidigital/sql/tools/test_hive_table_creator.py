import mock
import pytest

import itidigital.sql.athena.tools.hive_table_creator
from itidigital.data_quality.event.event import FieldType
from itidigital.utils.schema.event import EventSchema, ObjectField, SchemaField
from itidigital.sql.athena.hive.table import HiveTable
from itidigital.utils.schema.builder import SchemaBuilder
from itidigital.sql.athena.tools.hive_table_creator import HiveTableCreator, HiveType

from tests.test_data import examples


class TestHiveTableCreator:
    """Test class for `HiveTableCreator`"""

    @pytest.fixture
    def schema(self) -> EventSchema:
        """Fixture for Schema class example"""
        return SchemaBuilder(
            config=examples.EXAMPLE_SCHEMA
        ).construct()

    @pytest.fixture
    def hive_table_creator(self) -> HiveTableCreator:
        """Fixture for `HiveTableCreator` class example"""
        return HiveTableCreator()

    def test_from_event_schema_should_works_as_expected(
        self, schema: EventSchema, hive_table_creator: HiveTableCreator
    ) -> None:
        """Asserts that `from_event_schema` works as expected"""
        table = hive_table_creator.from_event_schema(
            event_schema=schema,
            **examples.TABLE_CONFIG
        )

        assert isinstance(table, HiveTable)

    def test_from_event_schema_should_raise_exception(
        self, schema: EventSchema, hive_table_creator: HiveTableCreator
    ) -> None:
        """Asserts that `from_event_schema` raises an exception"""
        fields = {
            "fields": {
                "type": "string"
            }
        }

        invalid_table_config = {
            **examples.TABLE_CONFIG,
            **fields
        }

        with pytest.raises(KeyError):
            hive_table_creator.from_event_schema(
                event_schema=schema,
                **invalid_table_config
            )

    def test__is_nested_type_should_works_as_expected(
        self, hive_table_creator: HiveTableCreator
    ) -> None:
        """Asserts that `_is_nested_type` works as expected"""
        nested_field = HiveType.OBJECT

        assert hive_table_creator._is_nested_type(
            field_type=nested_field
        )

    def test__json_to_hive_type_converter_should_works_as_expected(
        self, hive_table_creator: HiveTableCreator, schema: EventSchema
    ) -> None:
        """Asserts that `_json_to_hive_type_converter` works as expected"""
        converted_field = hive_table_creator._json_to_hive_type_converter(schema)

        assert converted_field.type == FieldType.OBJECT
        assert converted_field.properties[0].type == HiveType.STRING
        assert converted_field.properties[1].type == HiveType.STRING
        assert converted_field.properties[2].type == HiveType.STRING
        assert converted_field.properties[3].type == HiveType.INTEGER
        assert converted_field.properties[4].type == HiveType.OBJECT

    @mock.patch.object(
        target=itidigital.sql.athena.tools.hive_table_creator.HiveTableCreator,
        attribute="_map_regular_field",
        return_value={}
    )
    @mock.patch.object(
        target=itidigital.sql.athena.tools.hive_table_creator.HiveTableCreator,
        attribute="_map_struct_field",
        return_value={}
    )
    def test__map_fields_should_works_as_expected(
        self,
        map_regular_field_mock: mock.MagicMock,
        map_struct_field_mock: mock.MagicMock,
        hive_table_creator: HiveTableCreator,
        schema: EventSchema
    ) -> None:
        """Asserts that `_map_fields` works as expected"""
        expected_mapping = {'mailAddress': {}, 'number': {}, 'street': {}}

        field_mappings = hive_table_creator._map_fields(
            schema=schema.properties[4]
        )

        assert field_mappings == expected_mapping

    def test__map_regular_field_should_work_as_expected(
        self, hive_table_creator: HiveTableCreator, schema: EventSchema
    ) -> None:
        """Asserts that `_map_regular_field` works as expected"""
        expected_map = {
            'description': 'An explanation about the purpose of this instance.',
            'type': 'string'
        }

        field_map = hive_table_creator._map_regular_field(
            field=schema.properties[0]
        )

        assert field_map == expected_map

    @mock.patch.object(
        target=itidigital.sql.athena.tools.hive_table_creator.HiveTableCreator,
        attribute="_map_fields",
        return_value={}
    )
    def test__map_struct_field_should_work_as_expected(
        self,
        map_fields_mock: mock.MagicMock,
        hive_table_creator: HiveTableCreator,
        schema: EventSchema
    ) -> None:
        """Asserts that `_map_struct_field` works as expected"""
        expected_map = {
            'description': 'An explanation about the purpose of this instance.',
            'fields': {},
            'type': 'object'
        }

        struct_map = hive_table_creator._map_struct_field(
            field=schema.properties[4]
        )

        assert struct_map == expected_map
