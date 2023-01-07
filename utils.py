""" Utils for VoloBot"""
import json
from bs4 import BeautifulSoup
from discord import Embed
from discord.ext.commands import BadArgument, MissingRequiredArgument, TooManyArguments
from traceback import format_exception
from typing import Any, Union
from urllib.request import Request, urlopen


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


def get_ddb_spell(spell_name: str) -> Embed:
    """Get spell info from DnD Beyond

    Args:
        spell_name (`str`): name of the spell to lookup

    Returns:
        `Embed`: Discord embed containing spell info
    """
    spell_name = spell_name.replace(" ", "-")
    url = f"https://www.dndbeyond.com/spells/{spell_name}"

    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    # Open the url and parse the HTML
    with urlopen(req) as spell_page:
        # Parse the site's HTML using the Beautiful Soup web-scraping library
        # Note: 'html.parser' indicates the use of Python's native HTML parsing library.
        # 		The 'lxml' parser is slightly faster than Python's default, but it requires the installation of a third-party module. https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser
        # 		For this reason, I have decided to use the default parser for consistency across devices.
        parsed_html = BeautifulSoup(spell_page, "html.parser")

    spell_name = parsed_html.find("h1", class_="page-title").text

    spell_description = parsed_html.find("div", class_="more-info-content").get_text("\n\n", True)

    spell_dict = {"description": spell_description}

    items = {
        "Level": "level",
        "Casting Time": "casting-time",
        "Range": "range-area",
        "Components": "components",
        "Duration": "duration",
        "School": "school",
        "Attack/Save": "attack-save",
        "Damage Effect": "damage-effect",
    }

    for k, v in items.items():
        spell_dict[k] = get_statblock_value(v, parsed_html)

    spell_dict["Source"] = url

    return dict_to_embed(spell_name, spell_dict)


def get_statblock_value(item_name, parsed_html):
    item = parsed_html.find("div", class_=f"ddb-statblock-item ddb-statblock-item-{item_name}")
    return item.find("div", class_="ddb-statblock-item-value").get_text(";", True).split(";")[0]
