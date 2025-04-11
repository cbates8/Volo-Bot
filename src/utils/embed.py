"""Discord Embed Utils"""

from discord import Embed


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
        elif key == "content" and isinstance(value, list):
            formatted_values = ""
            for line in value:
                formatted_values += f"{line}\n\n"
            embed.description = formatted_values
        else:
            if isinstance(value, dict):
                formatted_values = ""
                for k, v in value.items():
                    formatted_values += f"{k}: {v}\n\n"
            else:
                formatted_values = value
            embed.add_field(name=key, value=formatted_values, inline=False)
    return embed


def create_error_embed(error: Exception) -> Embed:
    """Create a Discord Embed describing a Python Exception

    Args:
        error (`Exception`): An error encountered by the program

    Returns:
        `Embed`: A Discord embed object with a description of the error, as well as traceback
    """
    embed = Embed(title="I've encountered an error:")
    embed.add_field(
        name=type(error).__name__,
        value=f"`{error}`",
        inline=False,
    )
    return embed
