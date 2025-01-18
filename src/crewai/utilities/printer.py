"""Utility for colored console output."""

from typing import Optional


class Printer:
    """Handles colored console output formatting."""

    def print(self, content: str, color: Optional[str] = None):
        if color in self.color_codes:
            formatted_content = f"{self.color_codes[color]} {content}{self.reset_code}"
        else:
            formatted_content = content
        print(formatted_content)

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
        self.color_codes = {
            "purple": "\033[95m",
            "red": "\033[91m",
            "bold_green": "\033[1m\033[92m",
            "bold_purple": "\033[1m\033[95m",
            "bold_blue": "\033[1m\033[94m",
            "yellow": "\033[93m",
            "bold_yellow": "\033[1m\033[93m",
        }
        self.reset_code = "\033[00m"
        self.bold_code = "\033[1m"
        self.final_result_prefix = "\033[1m\033[95m ## Final Result:\033[00m \033[92m"
        self.final_result_suffix = "\033[00m"
