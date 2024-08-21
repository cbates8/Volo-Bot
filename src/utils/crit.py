"""Critical Hit/Miss Utils"""

from typing import Union

import aiofiles
from aiocsv import AsyncDictReader

from constants.paths import CRIT_TABLE_PATH, FUMBLE_TABLE_PATH

#########################
### Input Validation ####
#########################


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

    for full_dmg_type in valid_types:
        # Includes abreviation support for damge types (spelling bludgeoning is hard!)
        if input_type in (full_dmg_type, full_dmg_type[:2]):
            return full_dmg_type
    return False


async def get_crit_result(crit_percentage: int, dmg_type: str) -> str:
    """Get critical hit result given a percentage and damage type

    Args:
        crit_percentage (`int`): Percentage representing critical hit severity
        dmg_type (`str`): Type of damage being inflicted

    Returns:
        `str`: Description of the crit result
    """
    if validate_crit_percentage(crit_percentage):
        # Opens 'Critical_Hit_Table.csv' and treats it as a dictionary.
        # First row treated as keys, with following rows each being its own set of values for those keys
        async with aiofiles.open(CRIT_TABLE_PATH, mode="r", encoding="utf8") as csvfile:
            csvreader = AsyncDictReader(csvfile)
            fieldnames = await csvreader.get_fieldnames()
            roll_values = fieldnames[0]
            valid_dmg_types = fieldnames[1:]

            dmg_type = validate_damage_type(valid_dmg_types, dmg_type)
            if dmg_type:
                async for row in csvreader:
                    # Uses 'row' as the dictionary identifier and finds the value assigned to key 'dmg_type'
                    if int(row[roll_values]) == crit_percentage:
                        response = row[dmg_type]
                        break
            else:
                # using chr(10) as newline, because f-string doesn't support \n in expression part
                response = f"**Error:** Invalid Damage Type\nSupported types: ```\n{chr(10).join(valid_dmg_types)}```"
    else:
        response = "**Error:** Invalid Percentage Roll\nMust be value from 1-100"
    return response


async def get_fumble_result(fumble_percentage: int) -> str:
    """Get critical miss result given a percentage

    Args:
        fumble_percentage (`int`): Percentage representing critical miss severity

    Returns:
        `str`: Description of the fumble result
    """
    if validate_crit_percentage(fumble_percentage):
        # Opens 'Critical_Hit_Table.csv' and treats it as a dictionary.
        # First row treated as keys, with following rows each being its own set of values for those keys
        async with aiofiles.open(FUMBLE_TABLE_PATH, mode="r", encoding="utf8") as csvfile:
            csvreader = AsyncDictReader(csvfile)
            fieldnames = await csvreader.get_fieldnames()
            roll_values = fieldnames[0]
            fumble_effects = fieldnames[1]

            async for row in csvreader:
                # Uses 'row' as the dictionary identifier and finds the value assigned to key 'fumble_effects'
                if int(row[roll_values]) == fumble_percentage:
                    response = row[fumble_effects]
                    break
    else:
        response = "**Error:** Invalid Percentage Roll\nMust be value from 1-100"
    return response
