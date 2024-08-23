"""Spell Scraping Utils"""

from typing import Union
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup
from discord import Embed

from constants.paths import SPELLS_PATH
from utils.embed import dict_to_embed
from utils.json_utils import read_json_async

# Dict containing categories of spell information.
# Keys are the pretty title to be used in the Embed,
# values are the name of the HTML object to scrape
SPELL_ATTRIBUTES = {
    "Level": "level",
    "Casting Time": "casting-time",
    "Range": "range-area",
    "Components": "components",
    "Duration": "duration",
    "School": "school",
    "Attack/Save": "attack-save",
    "Damage Type": "damage-effect",
}
LOCAL_SOURCES = ["all", "local"]
ONLINE_SOURCES = ["all", "web"]
VALID_SOURCES = ["all", "local", "web"]


def get_statblock_value(item_name: str, parsed_html: BeautifulSoup) -> str:
    """
    Extract all text from a ddb-statblock-item

    Args:
        item_name (`str`): Name of the statblock-item to scrape
        parsed_html (`BeautifulSoup`): HTML of the site containing the statblocks

    Returns:
        `str`: Scraped text from ddb
    """
    # Identify the item containing the information we want
    item = parsed_html.find("div", class_=f"ddb-statblock-item ddb-statblock-item-{item_name}")

    # Get all text containied in the value section of the statblock
    return item.find("div", class_="ddb-statblock-item-value").get_text(";", True).split(";")[0]


def get_spell_from_ddb(spell_name: str) -> Embed:
    """Scrape spell info from DnD Beyond (https://www.dndbeyond.com/spells/{spell-name})

    Args:
        spell_name (`str`): Name of the spell to lookup

    Returns:
        `Embed`: Discord embed containing spell info
    """
    spell_name = spell_name.replace(" ", "-")
    url = f"https://www.dndbeyond.com/spells/{spell_name}"

    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    # Open the url and parse the HTML
    with urlopen(req) as spell_page:
        # Parse the site's HTML using the Beautiful Soup web-scraping library
        parsed_html = BeautifulSoup(spell_page, "html.parser")

    # Get the name of the spell from the page title
    spell_name = parsed_html.find("h1", class_="page-title").text

    # Get the spell description from the page content
    spell_description = parsed_html.find("div", class_="more-info-content").get_text("\n\n", True)

    # Create a dict to store spell information. Will be turned into an Embed later
    spell_dict = {"description": spell_description}

    # Scrape each spell attribute and add to the dictionary
    for label, item in SPELL_ATTRIBUTES.items():
        spell_dict[label] = get_statblock_value(item, parsed_html)

    # Add ddb page url to the dictonary
    spell_dict["Source"] = url

    return dict_to_embed(spell_name, spell_dict)


async def get_spell_from_file(spell_name: str) -> Embed:
    """Get spell info from local JSON file

    Args:
        spell_name (`str`): Name of the spell to lookup

    Returns:
        `Embed`: Discord embed containing spell info
    """
    # Search local spell file for information
    known_spells = await read_json_async(SPELLS_PATH)

    for name, description in known_spells.items():
        if spell_name.lower() == name.lower():
            embed = dict_to_embed(name, description)
            return embed


async def get_spell(spell_name: str, source: str = "all") -> Union[str, Embed]:
    """Get a spell from a local file or online

    Args:
        spell_name (`str`): Name of the spell to lookup
        source (`str`): Source to check. Defaults to 'all'

    Returns:
        `Union[str, Embed]`: Spell as a Discord embed, or an error message
    """
    # Validate source
    source = source.lower()
    if source not in VALID_SOURCES:
        return f"**Error:** Invalid Source '{source}'\nMust be one of: `{' | '.join(VALID_SOURCES)}`"

    # Check for the spell locally
    if source in LOCAL_SOURCES:
        response = await get_spell_from_file(spell_name)
        if source == "local":
            response = f"**Error:** Cannot find spell locally '{spell_name}'"

        # If we have a non-null response, we can return
        # If not, source must be 'all' so we will go check ddb
        if response:
            return response

    # Check for the spell online (via ddb)
    if source in ONLINE_SOURCES:
        try:
            response = get_spell_from_ddb(spell_name)
        except HTTPError:
            response = f"**Error:** Cannot find spell '{spell_name}'"
        return response
