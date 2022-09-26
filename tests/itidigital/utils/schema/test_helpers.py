import mock

from itidigital.utils.schema.helpers import load_schema


@mock.patch("builtins.open", create=True)
def test_load_schema_should_works_as_expected(mock_open):
    """Asserts that `load_schema` works as expected"""
    mock_open.side_effect = [
        mock.mock_open(read_data='{"foo": "bar"}').return_value
    ]

    schema = load_schema(
        file_path='my_schema.json'
    )

    assert schema == {"foo": "bar"}
