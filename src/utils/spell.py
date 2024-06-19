"""Spell Scraping Utils"""

from urllib.request import Request, urlopen

from bs4 import BeautifulSoup
from discord import Embed

from src.utils.embed import dict_to_embed


def get_ddb_spell(spell_name: str) -> Embed:
    """Scrape spell info from DnD Beyond (https://www.dndbeyond.com/spells/{spell-name})

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
        parsed_html = BeautifulSoup(spell_page, "html.parser")

    # Get the name of the spell from the page title
    spell_name = parsed_html.find("h1", class_="page-title").text

    # Get the spell description from the page content
    spell_description = parsed_html.find("div", class_="more-info-content").get_text("\n\n", True)

    # Create a dict to store spell information. Will be turned into an Embed later
    spell_dict = {"description": spell_description}

    # Dict containing categories of spell information. Keys are the pretty title to be used in the Embed, values are the name of the HTML object to scrape
    spell_details = {
        "Level": "level",
        "Casting Time": "casting-time",
        "Range": "range-area",
        "Components": "components",
        "Duration": "duration",
        "School": "school",
        "Attack/Save": "attack-save",
        "Damage Type": "damage-effect",
    }

    # Scrape each spell detail and add to the dictionary
    for label, item in spell_details.items():
        spell_dict[label] = get_statblock_value(item, parsed_html)

    # Add ddb page url to the dictonary
    spell_dict["Source"] = url

    return dict_to_embed(spell_name, spell_dict)


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
