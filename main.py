import json
import os
from typing import List, Any


def validate_array(*, node: list, schema: dict, node_path: str) -> List[str]:
    schema_items = schema["items"]

    errors = []

    for index, element in enumerate(node):
        node_errors = validate_node(node=element, schema=schema_items, node_path=f"{node_path}[{index}]")
        errors.extend(node_errors)

    return errors


def validate_object(*, node: Any, schema: dict, node_path: str) -> List[str]:
    errors = []

    required_fields = schema.get("required", [])
    for required_field in required_fields:
        if required_field not in node:
            errors.append(f"Field {node_path}.{required_field} is required!")

    properties_schemas = schema.get("properties", {})
    for property_field in properties_schemas:
        if property_field not in node:
            continue

        node_errors = validate_node(
            node=node[property_field],
            schema=properties_schemas[property_field],
            node_path=f"{node_path}.{property_field}",
        )
        errors.extend(node_errors)

    return errors


def validate_value(*, node: Any, type_name: str, schema: dict, node_path: str) -> List[str]:
    if type_name == "object":
        return validate_object(node=node, schema=schema, node_path=node_path)

    if type_name == "array":
        return validate_array(node=node, schema=schema, node_path=node_path)

    return []


def validate_type(*, node: Any, type_name: str) -> bool:
    if type_name == "number" and type(node) in (int, float):
        return True

    if type_name == "null" and node is None:
        return True

    if type_name == "string" and type(node) is str:
        return True

    if type_name == "object" and type(node) is dict:
        return True

    if type_name == "array" and type(node) is list:
        return True

    if type_name == "integer" and type(node) is int:
        return True

    if type_name == "boolean" and type(node) is bool:
        return True

    return False


def validate_node(*, node: Any, schema: dict, node_path: str) -> List[str]:
    errors = []

    type_names = schema["type"]

    if not isinstance(type_names, list):
        type_names = [type_names]

    for type_name in type_names:
        is_valid_type = validate_type(node=node, type_name=type_name)

        if is_valid_type:
            value_errors = validate_value(node=node, type_name=type_name, schema=schema, node_path=node_path)
            errors.extend(value_errors)
            return errors

    type_names_str = " or ".join(type_names)
    errors.append(f"Node {node_path} should be {type_names_str} not {type(node).__name__}")

    return errors


def validate_file(*, event_filename: str) -> List[str]:
    errors = []

    with open(event_filename) as event_file:
        event_file_content = event_file.read()
        json_event_file_content = json.loads(event_file_content)

        if not json_event_file_content:
            errors.append(f"Content in {event_filename} is empty!")
            return errors

        schema_event_file = json_event_file_content["event"]

        if not schema_event_file:
            errors.append(f"There is no schema in {event_filename}!")
            return errors

        try:
            with open(os.path.join("schema", f"{schema_event_file}.schema")) as schema_file:
                json_schema_file = json.loads(schema_file.read())

                node_path = "data"
                event_data = json_event_file_content[node_path]
                if not event_data:
                    errors.append(f"There is no data in file {event_filename}")
                    return errors

                node_errors = validate_node(node=event_data, schema=json_schema_file, node_path=node_path)
                errors.extend(node_errors)
                return errors
        except OSError:
            errors.append(f"There is no schema with name {schema_event_file}!")
            return errors


def validate_files() -> None:
    event_dir_name = "event"

    for event_filename in os.listdir(event_dir_name):
        print(f"Validate {event_filename}:")
        event_full_path = os.path.join(event_dir_name, event_filename)
        validate_file_errors = validate_file(event_filename=event_full_path)

        if len(validate_file_errors):
            for validate_file_error in validate_file_errors:
                print(validate_file_error)
        else:
            print("Everything is OK!")
        print()


if __name__ == "__main__":
    validate_files()
