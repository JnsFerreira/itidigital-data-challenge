import pytest

from itidigital.data_quality.event.builder import (
    EventBuilder,
    EventFieldBuilder
)

from itidigital.data_quality.event.event import (
    Event,
    EventField,
    FieldType,
)


class TestEventFieldBuilder:
    """Test class for `EventFieldBuilder`"""

    @pytest.fixture
    def event_field_builder(self) -> EventFieldBuilder:
        """Fixture for EventFieldBuilder class example"""
        event_field = {
            "name": "foo",
            "value": "bar"
        }

        return EventFieldBuilder(config=event_field)

    @pytest.fixture
    def nested_event_field_builder(self) -> EventFieldBuilder:
        """Fixture for EventFieldBuilder class example"""
        event_field = {
            "name": "my_nested_field",
            "value": {"foo": "bar"}
        }

        return EventFieldBuilder(config=event_field)

    def test_construct_should_work_as_expected(self, event_field_builder: EventFieldBuilder) -> None:
        """Asserts that `construct` method works as expected"""
        expected_event_field = EventField(
            name="foo",
            value="bar",
            type=FieldType.STRING
        )

        event_field = event_field_builder.construct()

        assert event_field == expected_event_field

    def test_construct_should_return_expected_type(self, event_field_builder: EventFieldBuilder) -> None:
        """Asserts that `construct` method returns the expected type"""

        event_field = event_field_builder.construct()

        assert isinstance(event_field, EventField)

    def test_get_name_should_work_as_expected(self, event_field_builder: EventFieldBuilder) -> None:
        """Asserts that `get_name` method works as expected"""
        expected_name = "foo"
        event_name = event_field_builder.get_name()

        assert expected_name == event_name

    def test_get_type_should_work_as_expected(self, event_field_builder: EventFieldBuilder) -> None:
        """Asserts that `get_type` method works as expected"""
        expected_type = FieldType.STRING
        event_type = event_field_builder.get_type()

        assert expected_type == event_type

    def test_get_value_should_work_as_expected(self, event_field_builder: EventFieldBuilder) -> None:
        """Asserts that `get_value` method works as expected"""
        expected_value = "bar"
        event_value = event_field_builder.get_value()

        assert expected_value == event_value

    def test__get_value_for_object_fields_should_work_as_expected(
            self, nested_event_field_builder: EventFieldBuilder
    ) -> None:
        """Asserts that `_get_value_for_object_fields` method works as expected"""
        expected_nested_field = [
            EventField(
                name='foo',
                value='bar',
                type=FieldType.STRING
            )
        ]

        nested_field = nested_event_field_builder._get_value_for_object_fields()

        assert nested_field == expected_nested_field


class TestEventBuilder:
    """Test class for `EventBuilder`"""

    @pytest.fixture
    def event_builder(self) -> EventBuilder:
        """Fixture for `EventBuilder` class example"""
        event = {
            "foo": "bar"
        }

        return EventBuilder(config=event)

    def test_construct_should_work_as_expected(self, event_builder: EventBuilder) -> None:
        """Asserts that `construct` method works as expected"""
        expected_event = Event(
            fields=[
                EventField(
                    name="foo",
                    value="bar",
                    type=FieldType.STRING
                )
            ]
        )

        event = event_builder.construct()

        assert event == expected_event

    def test_get_fields_should_work_as_expected(self, event_builder: EventBuilder) -> None:
        """Asserts that `get_fields` method works as expected"""
        expected_fields = [
            EventField(
                name="foo",
                value="bar",
                type=FieldType.STRING
            )
        ]

        fields = event_builder.get_fields()

        assert fields == expected_fields
