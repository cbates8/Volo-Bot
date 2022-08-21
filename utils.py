""" Utils for VoloBot"""
import json
from traceback import format_exception
from typing import Any, Union
from discord import Embed
from discord.ext.commands import BadArgument, MissingRequiredArgument, TooManyArguments


def print_list(target: list[str]) -> None:
    """Neatly print a Python list object

    Args:
        target (`list[str]`): List object to print
    """
    for item in target:
        print(item, end="")


def print_error(error: Any) -> None:
    """Print error and traceback (if neccessary)

    Args:
        error (`Any`): Error caught by the program
    """
    print(f"\n{type(error)}: {error}\n-----")
    if type(error) not in (BadArgument, MissingRequiredArgument, TooManyArguments):
        print_list(format_exception(type(error), error, error.__traceback__))


def create_error_embed(error: Any) -> Embed:
    """Create a Discord Embed describing a Python Exception

    Args:
        error (`Any`): An error encountered by the program

    Returns:
        `Embed`: A Discord embed object with a description of the error, as well as traceback
    """
    embed = Embed(title="I've encountered an error:")

    if isinstance(error, BadArgument):
        embed.add_field(
            name="Bad Argument",
            value="An argument was passed as an incorrect type.",
            inline=False,
        )
    elif isinstance(error, MissingRequiredArgument):
        embed.add_field(
            name="Missing Required Argument",
            value="Send '!help <command>' to learn more about a command.",
            inline=False,
        )
    elif isinstance(error, TooManyArguments):
        embed.add_field(
            name="Too Many Arguments",
            value="Send '!help <command>' to learn more about a command.",
            inline=False,
        )
    else:
        embed.add_field(name="Exception Thrown", value="Yikes!", inline=False)
    embed.add_field(name="Error Text:", value=f"`{error}`", inline=False)
    return embed


def validate_crit_percentage(input_percentage: int) -> bool:
    """Validate user input crit percentage

    Args:
        input_percentage (`int`): User input percentage representing critical hit severity

    Returns:
        `bool`: True if input is valid, False otherwise.
    """
    return input_percentage in range(1, 101)


def validate_damage_type(valid_types: list[str], input_type: str) -> Union[str, bool]:
    """Validate user input damage type

    Args:
        valid_types (`list[str]`): List of valid damage types
        input_type (`str`): User input damage type

    Returns:
        `bool`: True if input is valid, False otherwise.
    """
    input_type = input_type.lower()

    for dmg_type in valid_types:
        if input_type in (
            dmg_type,
            dmg_type[:2],
        ):  # Includes abreviation support for damge types (spelling bludgeoning is hard!)
            return dmg_type
    return False


def load_json(file_path: str) -> Union[list, dict]:
    """Open and deserialize a JSON file to a Python object

    Args:
        file_path (`str`): Path to JSON file

    Returns:
        `Union[list, dict]`: Deserialized JSON as a Python object
    """
    with open(file_path, mode="r", encoding="utf8") as jsonfile:
        deserialized_json = json.load(jsonfile)
    return deserialized_json


def write_json(file_path: str, content: Union[list, dict]) -> None:
    """Serialize a Python object to a JSON string and write to a file

    Args:
        file_path (`str`): Path to JSON file
        content (`Union[list, dict]`): Python object to convert to JSON
    """
    with open(file_path, mode="w", encoding="utf8") as jsonfile:
        jsonfile.write(json.dumps(content, indent=4))


def dict_to_embed(title: str, content: dict) -> Embed:
    """Convert a dict object to a Discord Embed object

    Args:
        title (`str`): Title of the Embed
        content (`dict`): Content of the Embed

    Returns:
        `Embed`: Discord Embed object
    """

    embed = Embed(title=title)
    for field in content:
        if field == "description":
            embed.description = content[field]
        else:
            if isinstance(content[field], dict):
                formatted_values = ""
                for key, value in content[field]:
                    formatted_values += f"{key}: {value}\n\n"
            else:
                formatted_values = content[field]
            embed.add_field(name=field, value=formatted_values, inline=False)

    return embed
