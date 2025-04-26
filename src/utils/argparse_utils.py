"""ArgParse Utils"""

import argparse
from typing import Optional

NONE_EQUIVALENT = ["none", "None", "null", "Null", ""]


def none_or_str(value: str) -> Optional[str]:
    """Get Nonetype if possible, otherwise return string

    Args:
        value (`str`): Argument value

    Returns:
        `Optional[str]`: Value as a string or None
    """
    if value in NONE_EQUIVALENT:
        return None
    return str(value)


def none_or_int(value: str) -> Optional[int]:
    """Get Nonetype if possible, otherwise return int

    Args:
        value (`str`): Argument value

    Returns:
        `Optional[int]`: Value converted to int or None
    """
    if value in NONE_EQUIVALENT:
        return None
    return int(value)


class ArgParseError(Exception):
    """An generic error from argparse"""

    def __init__(self, message, usage=None):
        self.message = message
        self.usage = usage

    def __str__(self):
        if self.usage is None:
            msg_format = "%(message)s"
        else:
            msg_format = "%(usage)s\n%(message)s"
        return msg_format % dict(message=self.message, usage=self.usage)


class CustArgParser(argparse.ArgumentParser):
    """Custom ArgumentParser"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def error(self, message):
        """Overload of argparse.ArgumentParser.error

        Raises an exception instead of exiting the program.
        """
        raise ArgParseError(message, usage=self.format_usage())
