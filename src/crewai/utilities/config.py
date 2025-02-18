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

    model_fields = model_class.model_fields

    for key, value in config.items():
        if key in model_fields and values.get(key) is None:
            if isinstance(value, dict):
                current_value = values.get(key)
                if isinstance(current_value, dict):
                    current_value.update(value)
                else:
                    values[key] = value
            else:
                values[key] = value

    values.pop("config", None)  # Remove config to avoid future duplication
    return values
