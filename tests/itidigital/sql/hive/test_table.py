import pytest

from itidigital.sql.athena.hive.properties import *
from itidigital.sql.athena.hive.table import HiveTable
from itidigital.sql.athena.exceptions import InvalidRowFormatError, InvalidS3LocationError


class TestHiveTable:
    """Test class for `HiveTable`"""

    @pytest.fixture
    def hive_table(self) -> HiveTable:
        """Fixture for HiveTable class example"""
        return HiveTable(
            create_disposition=CreateDisposition.IF_NOT_EXISTS,
            table_reference=TableReference(
                database='itidigital',
                table_name='test_table'
            ),
            fields={
                "foo": {
                    "type": "string"
                },
                "bar": {
                    "type": "string"
                }
            },
            is_external=True,
            location='s3://my-bucket/itidigital/test_table',
            stored_as=FileFormat.PARQUET,
            comment='My test table',
            partition_by=['foo'],
            clustered_by=['bar'],
            num_buckets=10,
            row_format=DelimiterFormat(
                delimiter=Delimiter.DELIMITED_FIELDS_TERMINATED_BY,
                char=','
            ),
            table_properties={
                "my_prop": "my_value"
            }
        )

    def test_table_type_property_should_works_as_expected(
            self, hive_table: HiveTable
    ) -> None:
        """Asserts that `table_type` property works as expected"""
        expected_table_type = 'EXTERNAL TABLE'

        assert hive_table.table_type == expected_table_type

    def test_create_disposition_property_should_works_as_expected(
            self, hive_table: HiveTable
    ) -> None:
        """Asserts that `create_disposition` property works as expected"""
        expected_create_disposition = 'IF NOT EXISTS'

        assert hive_table.create_disposition == expected_create_disposition

    def test_table_name_property_should_works_as_expected(
            self, hive_table: HiveTable
    ) -> None:
        """Asserts that `table_name` property works as expected"""
        expected_table_name = 'itidigital.test_table'

        assert hive_table.table_name == expected_table_name

    def test_fields_property_should_works_as_expected(
            self, hive_table: HiveTable
    ) -> None:
        """Asserts that `fields` property works as expected"""
        expected_fields = 'foo string, \n\tbar string'

        assert hive_table.fields == expected_fields

    def test_comment_property_should_works_as_expected(
            self, hive_table: HiveTable
    ) -> None:
        """Asserts that `comment` property works as expected"""
        expected_comment = 'My test table'

        assert hive_table.comment == expected_comment

    def test_partition_by_property_should_works_as_expected(
            self, hive_table: HiveTable
    ) -> None:
        """Asserts that `partition_by` property works as expected"""
        expected_partition = 'foo'

        assert hive_table.partition_by == expected_partition

    def test_clustered_by_property_should_works_as_expected(
            self, hive_table: HiveTable
    ) -> None:
        """Asserts that `clustered_by` property works as expected"""
        expected_cluster = 'bar'

        assert hive_table.clustered_by == expected_cluster

    def test_num_buckets_property_should_works_as_expected(
            self, hive_table: HiveTable
    ) -> None:
        """Asserts that `num_buckets` property works as expected"""
        expected_num_buckets = 10

        assert hive_table.num_buckets == expected_num_buckets

    def test_row_format_property_should_works_as_expected(
            self, hive_table: HiveTable
    ) -> None:
        """Asserts that `row_format` property works as expected"""
        expected_row_format = 'DELIMITED FIELDS TERMINATED BY ,'

        assert hive_table.row_format == expected_row_format

    def test_row_format_should_raise_exception(
        self, hive_table: HiveTable
    ) -> None:
        """Asserts that `row_format` throws an exception"""
        with pytest.raises(InvalidRowFormatError):
            hive_table.row_format = "INVALID ROW FORMAT"

    def test_location_should_works_as_expected(
        self, hive_table: HiveTable
    ) -> None:
        """Asserts that `location` property works as expected"""
        expected_location = 's3://my-bucket/itidigital/test_table'

        assert hive_table.location == expected_location

    @pytest.mark.parametrize('invalid_location', ['s4://', 's3://my-bucket/folder/*'])
    def test_location_should_raise_exception(
        self, hive_table: HiveTable, invalid_location: str
    ) -> None:
        """Asserts that `location` property throws an exception"""
        with pytest.raises(InvalidS3LocationError):
            hive_table.location = invalid_location

    def test_stored_as_should_works_as_expected(
        self, hive_table: HiveTable
    ) -> None:
        """Asserts that `stored_as` property works as expected"""
        expected_stored_as = 'parquet'

        assert hive_table.stored_as == expected_stored_as

    def test_table_properties_should_works_as_expected(
        self, hive_table: HiveTable
    ) -> None:
        """Asserts that `table_properties` property works as expected"""
        expected_table_properties = 'my_prop = my_value'

        assert hive_table.table_properties == expected_table_properties
