"""Utility for colored console output."""

from typing import Optional


class Printer:
    """Handles colored console output formatting."""

    def print(self, content: str, color: Optional[str] = None):
        color_map = {
            "purple": "\033[95m",
            "red": "\033[91m",
            "bold_green": "\033[1m\033[92m",
            "bold_purple": "\033[1m\033[95m",
            "bold_blue": "\033[1m\033[94m",
            "yellow": "\033[93m",
            "bold_yellow": "\033[1m\033[93m",
        }
        if color in color_map:
            print(f"{color_map[color]} {content}\033[00m")
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
