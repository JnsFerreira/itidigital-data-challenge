import mock
import pytest

import itidigital.data_quality.event.event
from itidigital.data_quality.event.event import (
    Event,
    EventField
)

from itidigital.data_quality.event.builder import (
    FieldType
)


class TestEvent:
    """Test class for `Event`"""

    @pytest.fixture
    def event(self) -> Event:
        """Fixture for Event class example"""
        return Event(
            fields=[
                EventField(
                    name="foo",
                    value="bar",
                    type=FieldType.STRING
                )
            ]
        )

    def test_json_schema_should_works_as_expected(
        self,
        event: Event
    ) -> None:
        """Asserts that `json_schema` property works as expected"""
        with mock.patch.object(
            itidigital.data_quality.event.event.Event,
            "_infer_schema",
            return_value={}
        ) as mock_method:
            assert event.json_schema == mock_method.return_value

    def test__infer_schema_should_be_called_by_json_schema(
        self, event: Event
    ) -> None:
        """Asserts that `_infer_schema` method is called by json_schema property"""
        event._infer_schema = mock.MagicMock()

        schema = event.json_schema

        event._infer_schema.assert_called()

    def test__infer_schema_should_works_as_expected(
        self, event: Event
    ) -> None:
        """Asserts that `_infer_schema` method works as expected"""
        expected_schema = {
            "$schema": "http://json-schema.org/draft-07/schema",
            "$id": "http://example.com/example.json",
            "type": "object",
            "title": "The root schema",
            "description": "The root schema comprises the entire JSON document.",
            "required": [
            ],
            "properties": {}
        }

        with mock.patch.object(
            itidigital.data_quality.event.event.Event,
            "_get_properties",
            return_value={"properties": {}}
        ):
            schema = event._infer_schema(fields=event.fields)

            assert schema == expected_schema

    def test__get_properties_should_be_called_by_infer_schema(
        self, event: Event
    ) -> None:
        """Asserts that `_get_properties` method is called by `_infer_schema`"""
        event._get_properties = mock.MagicMock()

        schema = event._infer_schema(
            fields=event.fields
        )

        event._get_properties.assert_called()

    def test__get_properties_should_works_as_expected(
        self, event: Event
    ) -> None:
        """Asserts that `_get_properties` method works as expected"""
        expected_properties = {"properties": {"foo": {}}}

        with mock.patch.object(
            target=itidigital.data_quality.event.event.Event,
            attribute="_get_properties_for_regular_fields",
            return_value={}
        ):
            properties = event._get_properties(fields=event.fields)

            assert properties == expected_properties

    def test__get_properties_for_regular_fields_is_called(
        self, event: Event
    ) -> None:
        """Asserts that `_get_properties_for_regular_fields` method is called by `_get_properties`"""
        event._get_properties_for_regular_fields = mock.MagicMock()

        properties = event._get_properties(
            fields=event.fields
        )

        event._get_properties_for_regular_fields.assert_called()

    def test__get_properties_for_object_fields_is_called(
        self, event: Event
    ) -> None:
        """Asserts that `_get_properties_for_regular_fields` method is called by `_get_properties`"""
        event.fields = [
            EventField(
                name="nested_field",
                value={"foo", "bar"},
                type=FieldType.OBJECT
            )
        ]

        event._get_properties_for_object_fields = mock.MagicMock()
        event._get_properties(fields=event.fields)

        event._get_properties_for_object_fields.assert_called()

    def test__get_properties_for_object_fields_should_works_as_expected(
        self, event: Event
    ):
        """Asserts that `_get_properties_for_object_fields` method works as expected"""
        expected_property = {
            '$id': 'nested_field',
            'properties': {
                'foo': {
                    '$id': 'foo',
                    'description': 'foo field of type string',
                    'examples': ['bar'],
                    'title': 'foo field',
                    'type': 'string'
                }
            },
            'type': 'object'
        }

        object_properties = event._get_properties_for_object_fields(
            field=EventField(
                    name="nested_field",
                    value=[
                        EventField(
                            name="foo",
                            value="bar",
                            type=FieldType.STRING
                        )
                    ],
                    type=FieldType.OBJECT
                )
        )

        assert object_properties == expected_property

    def test__get_properties_for_regular_fields_should_works_as_expected(
        self, event: Event
    ):
        """Asserts that `_get_properties_for_regular_fields` method works as expected"""
        expected_field_property = {
            '$id': 'foo',
            'description': 'foo field of type string',
            'examples': ['bar'],
            'title': 'foo field',
            'type': 'string',

        }

        field_property = event._get_properties_for_regular_fields(
            field=EventField(
                name="foo",
                value="bar",
                type=FieldType.STRING
            )
        )

        assert field_property == expected_field_property
