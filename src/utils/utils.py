"""Utils for VoloBot"""

import aiofiles
import json
from typing import Union

from constants.paths import COG_PATH


def get_cog_path(cog: str) -> str:
    """Get dot path of a cog
    e.g. `spell` -> `commands.spell`

    Args:
        cog (`str`): Name of a cog

    Returns:
        `str`: Dot path of a cog
    """
    return COG_PATH.format(cog=cog.lower())


###############################
### Input validation utils ####
###############################


def validate_crit_percentage(input_percentage: int) -> bool:
    """Validate user input crit percentage.
    Percentage should be an integer between 1 and 100 (inclusive)

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
        `Union[str, bool]`: damage type if it is valid, False otherwise.
    """
    input_type = input_type.lower()

    for dmg_type in valid_types:
        # Includes abreviation support for damge types (spelling bludgeoning is hard!)
        if input_type in (dmg_type, dmg_type[:2]):
            return dmg_type
    return False


#################################
### Data transformation utils ###
#################################


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
