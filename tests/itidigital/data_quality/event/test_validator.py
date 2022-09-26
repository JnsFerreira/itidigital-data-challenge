import pytest

from tests.test_data import examples

from itidigital.utils.schema.event import EventSchema
from itidigital.utils.schema.builder import SchemaBuilder
from itidigital.data_quality.event.builder import EventBuilder
from itidigital.data_quality.event.validator import EventValidator
from itidigital.data_quality.event.exceptions import InvalidSchemaObject


class TestEventValidator:
    """Test class for EventValidator"""

    @pytest.fixture
    def schema(self):
        """Fixture for Schema class example"""
        return SchemaBuilder(
            config=examples.EXAMPLE_SCHEMA
        ).construct()

    @pytest.fixture
    def event_validator(self, schema) -> EventValidator:
        """Fixture for EventValidator class example"""
        return EventValidator(
            schema=schema
        )

    def test_schema_property_works_as_expected(
        self,
        event_validator: EventValidator,
        schema: EventSchema
    ) -> None:
        """Asserts that `schema` property works as expected"""
        assert event_validator.schema == schema

    def test_schema_setter_should_works_as_expected(
        self,
        event_validator: EventValidator,
        schema: EventSchema
    ) -> None:
        """Asserts that `schema` setter works as expected"""
        schema.properties = {}
        event_validator.schema = schema

        assert event_validator.schema == schema

    def test_schema_setter_should_throws_exception(
        self, event_validator: EventValidator
    ) -> None:
        """Asserts that `schema` setter raises InvalidSchemaObject error"""
        with pytest.raises(InvalidSchemaObject):
            event_validator.schema = 'INVALID_SCHEMA_OBJECT'

    def test_id_valid_should_works_as_expected(
        self, event_validator: EventValidator
    ) -> None:
        """Asserts that `is_valid` method works as expected"""
        event = EventBuilder(
            config=examples.EXAMPLE_EVENT
        ).construct()

        assert event_validator.is_valid(
            event=event
        )
