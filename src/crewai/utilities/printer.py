"""Utility for colored console output."""

import json
from functools import lru_cache
from typing import Optional, Type

from pydantic import BaseModel, ValidationError


class Printer:
    """Handles colored console output formatting."""

    def print(self, content: str, color: Optional[str] = None):
        color_methods = {
            "purple": self._print_purple,
            "red": self._print_red,
            "bold_green": self._print_bold_green,
            "bold_purple": self._print_bold_purple,
            "bold_blue": self._print_bold_blue,
            "yellow": self._print_yellow,
            "bold_yellow": self._print_bold_yellow,
        }
        if color in color_methods:
            color_methods[color](content)
        else:
            print(content)

    def _print_bold_purple(self, content):
        print("\033[1m\033[95m {}\033[00m".format(content))

    def _print_bold_green(self, content):
        print("\033[1m\033[92m {}\033[00m".format(content))

    def _print_purple(self, content):
        print("\033[95m {}\033[00m".format(content))

    def _print_red(self, content):
        print("\033[91m {}\033[00m".format(content))

    def _print_bold_blue(self, content):
        print("\033[1m\033[94m {}\033[00m".format(content))

    def _print_yellow(self, content):
        print("\033[93m {}\033[00m".format(content))

    def _print_bold_yellow(self, content):
        print("\033[1m\033[93m {}\033[00m".format(content))


@lru_cache(maxsize=None)
def cached_model_validate_json(model: Type[BaseModel], json_string: str):
    try:
        return model.model_validate_json(json_string)
    except (json.JSONDecodeError, ValidationError) as e:
        return e
