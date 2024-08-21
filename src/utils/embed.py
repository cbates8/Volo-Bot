"""Discord Embed Utils"""

from typing import Any

from discord import Embed
from discord.ext.commands import BadArgument, MissingRequiredArgument, TooManyArguments


def dict_to_embed(title: str, content: dict) -> Embed:
    """Convert a dict object to a Discord Embed object

    Args:
        title (`str`): Title of the Embed
        content (`dict`): Content of the Embed

    Returns:
        `Embed`: Discord Embed object
    """
    embed = Embed(title=title)
    for key, value in content.items():
        if key == "description":
            embed.description = value
        else:
            if isinstance(value, dict):
                formatted_values = ""
                for k, v in value.items():
                    formatted_values += f"{k}: {v}\n\n"
            else:
                formatted_values = value
            embed.add_field(name=key, value=formatted_values, inline=False)

    return embed


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
