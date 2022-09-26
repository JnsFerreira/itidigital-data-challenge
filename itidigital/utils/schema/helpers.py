import json


def load_schema(file_path: str) -> dict:
    """
    Loads JSON schema from a given file path

    Args:
        file_path (str): file path where JSON schema is located

    Returns
        dict: JSON schema loaded as dictionary
    """
    with open(file_path, 'r') as schema_file:
        return json.loads(schema_file.read())
