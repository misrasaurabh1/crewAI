"""Utility for colored console output."""

from typing import Optional


class Printer:
    """Handles colored console output formatting."""

    def print(self, content: str, color: Optional[str] = None):
        color_code = self._color_codes.get(color, "")
        reset_code = "\033[00m" if color_code else ""
        print(f"{color_code} {content}{reset_code}")

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
