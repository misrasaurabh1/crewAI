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
        if key in values or key not in model_fields:
            continue

        if isinstance(value, dict):
            values[key] = {**value, **values.get(key, {})}
        else:
            values[key] = value

    values.pop("config", None)
    return values
