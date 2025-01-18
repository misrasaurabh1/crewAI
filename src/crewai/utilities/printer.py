"""Utility for colored console output."""

from typing import Optional


class Printer:
    """Handles colored console output formatting."""

    def print(self, content: str, color: Optional[str] = None):
        if color:
            print_method = self.color_methods.get(color)
            if print_method:
                print_method(content)
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

    def __init__(self):
        self.color_methods = {
            "purple": self._print_purple,
            "red": self._print_red,
            "bold_green": self._print_bold_green,
            "bold_purple": self._print_bold_purple,
            "bold_blue": self._print_bold_blue,
            "yellow": self._print_yellow,
            "bold_yellow": self._print_bold_yellow,
        }
