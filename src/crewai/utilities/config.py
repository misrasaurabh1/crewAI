from typing import Any, Dict, Type

from pydantic import BaseModel


def process_config(
    values: Dict[str, Any], model_class: Type[BaseModel]
) -> Dict[str, Any]:
    """
    Process the config dictionary and update the values accordingly.

    Args:
        values (Dict[str, Any]): The dictionary of values to update.
        model_class (Type[BaseModel]): The Pydantic model class to reference for field validation.

    Returns:
        Dict[str, Any]: The updated values dictionary.
    """
    config = values.get("config")
    if not config:
        return values

    # Initialize keys set from model fields for faster check
    model_fields_keys = model_class.model_fields.keys()

    # Efficiently update values using config by avoiding multiple lookups
    for key, value in config.items():
        if key not in model_fields_keys or values.get(key) is not None:
            continue

        if isinstance(value, dict):
            existing_value = values.get(key)
            if isinstance(existing_value, dict):
                existing_value.update(value)
            else:
                values[key] = value
        else:
            values[key] = value

    # Remove the config from values after processing to avoid duplication
    values.pop("config", None)
    return values
