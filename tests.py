from unittest.mock import mock_open, patch

from main import validate_type, validate_array, validate_object, validate_value, validate_node, validate_file


def test_validate_type__number_int():
    type_name = "number"
    node = 1

    assert validate_type(node=node, type_name=type_name)


def test_validate_type__number_str_int():
    type_name = "number"
    node = "1"

    assert not validate_type(node=node, type_name=type_name)


def test_validate_type__number_float():
    type_name = "number"
    node = 1.1

    assert validate_type(node=node, type_name=type_name)


def test_validate_type__null_none():
    type_name = "null"
    node = None

    assert validate_type(node=node, type_name=type_name)


def test_validate_type__string_str():
    type_name = "string"
    node = "abc"

    assert validate_type(node=node, type_name=type_name)


def test_validate_type__object_dict():
    type_name = "object"
    node = {}

    assert validate_type(node=node, type_name=type_name)


def test_validate_type__array_list():
    type_name = "array"
    node = []

    assert validate_type(node=node, type_name=type_name)


def test_validate_type__integer_int():
    type_name = "integer"
    node = 1

    assert validate_type(node=node, type_name=type_name)


def test_validate_type__boolean_bool():
    type_name = "boolean"
    node = False

    assert validate_type(node=node, type_name=type_name)


def test_validate_type__integer_bool():
    type_name = "integer"
    node = False

    assert not validate_type(node=node, type_name=type_name)


def test_validate_array__empty_list():
    node = []
    schema = {
        "items": {}
    }

    errors = validate_array(node=node, schema=schema, node_path="data")

    assert errors == []


def test_validate_array__int():
    node = [1, 2, 3, 4]
    schema = {
        "items": {
            "type": "integer"
        }
    }

    errors = validate_array(node=node, schema=schema, node_path="data")

    assert errors == []


def test_validate_array__object():
    node = [{"id": 1}, {"id": 2}, {"id": 3}]
    schema = {
        "items": {
            "type": "object",
        }
    }

    errors = validate_array(node=node, schema=schema, node_path="data")

    assert errors == []


def test_validate_array__list_in_list():
    node = [[1, 2], [3, 4], [5, 6]]
    schema = {
        "items": {
            "type": "array",
            "items": {
                "type": "integer",
            }
        }
    }

    errors = validate_array(node=node, schema=schema, node_path="data")

    assert errors == []


def test_validate_array__integer_str():
    node = [1, 2, "3"]
    schema = {
        "items": {
            "type": "integer",
        }
    }

    errors = validate_array(node=node, schema=schema, node_path="data")

    assert errors == ["Node data[2] should be integer not str"]


def test_validate_object__empty():
    node = {}
    schema = {}

    errors = validate_object(node=node, schema=schema, node_path="data")

    assert errors == []


def test_validate_object__required():
    node = {
        "id": 1,
        "name": "name",
        "surname": "surname",
    }
    schema = {
        "required": ["id", "name", "surname"]
    }

    errors = validate_object(node=node, schema=schema, node_path="data")

    assert errors == []


def test_validate_object__required_error():
    node = {
        "id": 1,
        "name": "name",
    }
    schema = {
        "required": ["id", "name", "surname"]
    }

    errors = validate_object(node=node, schema=schema, node_path="data")

    assert errors == ["Field data.surname is required!"]


def test_validate_object__properties():
    node = {
        "id": 1,
        "name": "name",
    }
    schema = {
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "surname": {"type": "string"},
        }
    }

    errors = validate_object(node=node, schema=schema, node_path="data")

    assert errors == []


def test_validate_object__properties__error_type():
    node = {
        "id": "1",
        "name": "name",
    }
    schema = {
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "surname": {"type": "string"},
        }
    }

    errors = validate_object(node=node, schema=schema, node_path="data")

    assert errors == ["Node data.id should be integer not str"]


def test_validate_value__simple_type():
    node = 1
    type_name = "integer"
    schema = {
        "type": "integer",
    }

    errors = validate_value(node=node, type_name=type_name, schema=schema, node_path="data")

    assert errors == []


def test_validate_value__empty_object():
    node = {}
    type_name = "object"
    schema = {
        "type": "object",
    }

    errors = validate_value(node=node, type_name=type_name, schema=schema, node_path="data")

    assert errors == []


def test_validate_value__valid_object():
    node = {
        "id": 1,
    }
    type_name = "object"
    schema = {
        "type": "object",
        "required": ["id"],
        "properties": {
            "id": {"type": "integer"}
        }
    }

    errors = validate_value(node=node, type_name=type_name, schema=schema, node_path="data")

    assert errors == []


def test_validate_value__invalid_object():
    node = {}
    type_name = "object"
    schema = {
        "type": "object",
        "required": ["id"],
        "properties": {
            "id": {"type": "integer"}
        }
    }

    errors = validate_value(node=node, type_name=type_name, schema=schema, node_path="data")

    assert errors == ["Field data.id is required!"]


def test_validate_value__empty_array():
    node = []
    type_name = "array"
    schema = {
        "type": "array",
        "items": {},
    }

    errors = validate_value(node=node, type_name=type_name, schema=schema, node_path="data")

    assert errors == []


def test_validate_value__valid_array():
    node = [1, 2, 3]
    type_name = "array"
    schema = {
        "type": "array",
        "items": {
            "type": "integer",
        },
    }

    errors = validate_value(node=node, type_name=type_name, schema=schema, node_path="data")

    assert errors == []


def test_validate_value__invalid_array():
    node = ["1", 2, 3]
    type_name = "array"
    schema = {
        "type": "array",
        "items": {
            "type": "integer",
        },
    }

    errors = validate_value(node=node, type_name=type_name, schema=schema, node_path="data")

    assert errors == ["Node data[0] should be integer not str"]


def test_validate_node__empty_object():
    node = {}
    schema = {
        "type": "object"
    }

    errors = validate_node(node=node, schema=schema, node_path="data")

    assert errors == []


def test_validate_node__valid_object():
    node = {
        "id": 1,
        "name": "name",
    }
    schema = {
        "type": "object",
        "required": ["id", "name"],
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "surname": {"type": "string"},
        }
    }

    errors = validate_node(node=node, schema=schema, node_path="data")

    assert errors == []


def test_validate_node__invalid_object():
    node = {
        "id": "1",
        "name": "name",
    }
    schema = {
        "type": "object",
        "required": ["id", "name"],
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "surname": {"type": "string"},
        }
    }

    errors = validate_node(node=node, schema=schema, node_path="data")

    assert errors == ["Node data.id should be integer not str"]


def test_validate_node__nested_object():
    node = {
        "person": {
            "id": 1,
            "name": "name",
        }
    }
    schema = {
        "type": "object",
        "required": ["person"],
        "properties": {
            "person": {
                "type": "object",
                "required": ["id", "name"],
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "surname": {"type": "string"},
                }
            },
        }
    }

    errors = validate_node(node=node, schema=schema, node_path="data")

    assert errors == []


def test_validate_node__invalidnested_object():
    node = {
        "person": {
            "id": "1",
            "name": "name",
        }
    }
    schema = {
        "type": "object",
        "required": ["person"],
        "properties": {
            "person": {
                "type": "object",
                "required": ["id", "name"],
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "surname": {"type": "string"},
                }
            },
        }
    }

    errors = validate_node(node=node, schema=schema, node_path="data")

    assert errors == ["Node data.person.id should be integer not str"]


def test_validate_node__several_types():
    node = {
        "person": {
            "id": 1,
            "name": "name",
        }
    }
    schema = {
        "type": ["object", "null"],
        "required": ["person"],
        "properties": {
            "person": {
                "type": "object",
                "required": ["id", "name"],
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "surname": {"type": "string"},
                }
            },
        }
    }

    errors = validate_node(node=node, schema=schema, node_path="data")

    assert errors == []


def test_validate_node__several_types_none():
    node = None
    schema = {
        "type": ["object", "null"],
        "required": ["person"],
        "properties": {
            "person": {
                "type": "object",
                "required": ["id", "name"],
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "surname": {"type": "string"},
                }
            },
        }
    }

    errors = validate_node(node=node, schema=schema, node_path="data")

    assert errors == []


def test_validate_node__several_types_error():
    node = []
    schema = {
        "type": ["object", "null"],
        "required": ["person"],
        "properties": {
            "person": {
                "type": "object",
                "required": ["id", "name"],
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "surname": {"type": "string"},
                }
            },
        }
    }

    errors = validate_node(node=node, schema=schema, node_path="data")

    assert errors == ["Node data should be object or null not list"]


def test_validate_file__empty_json():
    mock_file = mock_open(read_data='{}').return_value
    mock_opener = mock_open()
    mock_opener.side_effect = [mock_file]

    with patch("main.open", mock_opener) as m:
        m.return_value = "{}"
        errors = validate_file(event_filename="event_filename")

        assert errors == ["Content in event_filename is empty!"]


def test_validate_file__no_schema():
    mock_file = mock_open(read_data='{"event": ""}').return_value
    mock_opener = mock_open()
    mock_opener.side_effect = [mock_file]

    with patch("main.open", mock_opener) as m:
        errors = validate_file(event_filename="event_filename")

        assert errors == ["There is no schema in event_filename!"]


def test_validate_file__no_schema_file():
    mock_file = mock_open(read_data='{"event": "schema_filename"}').return_value
    mock_opener = mock_open()
    mock_opener.side_effect = [mock_file, IOError]

    with patch("main.open", mock_opener) as m:
        errors = validate_file(event_filename="event_filename")

        assert errors == ["There is no schema with name schema_filename!"]


def test_validate_file__no_data():
    mock_files = [
        mock_open(read_data='{"event": "schema_filename", "data": ""}').return_value,
        mock_open(read_data='{}').return_value,
    ]
    mock_opener = mock_open()
    mock_opener.side_effect = mock_files

    with patch("main.open", mock_opener) as m:
        errors = validate_file(event_filename="event_filename")

        assert errors == ["There is no data in file event_filename"]


def test_validate_file__valid_simple_data():
    mock_files = [
        mock_open(read_data='{"event": "schema_filename", "data": {"id": 1}}').return_value,
        mock_open(read_data='{"type": "object", "required": ["id"], "properties": {"id": {"type": "integer"}}}').return_value,
    ]
    mock_opener = mock_open()
    mock_opener.side_effect = mock_files

    with patch("main.open", mock_opener) as m:
        errors = validate_file(event_filename="event_filename")

        assert errors == []


def test_validate_file__invalid_simple_data():
    mock_files = [
        mock_open(read_data='{"event": "schema_filename", "data": {"id": "1"}}').return_value,
        mock_open(read_data='{"type": "object", "required": ["id"], "properties": {"id": {"type": "integer"}}}').return_value,
    ]
    mock_opener = mock_open()
    mock_opener.side_effect = mock_files

    with patch("main.open", mock_opener) as m:
        errors = validate_file(event_filename="event_filename")

        assert errors == ["Node data.id should be integer not str"]


def test_validate_file__valid_array_data():
    mock_files = [
        mock_open(read_data='{"event": "schema_filename", "data": {"ids": [1, 2, 3]}}').return_value,
        mock_open(read_data='''{
            "type": "object",
            "required": ["ids"],
            "properties": {"ids": {"type": "array", "items": {"type": "integer"}}}
        }''').return_value,
    ]
    mock_opener = mock_open()
    mock_opener.side_effect = mock_files

    with patch("main.open", mock_opener) as m:
        errors = validate_file(event_filename="event_filename")

        assert errors == []


def test_validate_file__invalid_array_data():
    mock_files = [
        mock_open(read_data='{"event": "schema_filename", "data": {"ids": ["1", 2, 3]}}').return_value,
        mock_open(read_data='''{
            "type": "object",
            "required": ["ids"],
            "properties": {"ids": {"type": "array", "items": {"type": "integer"}}}
        }''').return_value,
    ]
    mock_opener = mock_open()
    mock_opener.side_effect = mock_files

    with patch("main.open", mock_opener) as m:
        errors = validate_file(event_filename="event_filename")

        assert errors == ["Node data.ids[0] should be integer not str"]
