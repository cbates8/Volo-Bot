"""Critical Hit/Miss Utils"""

from typing import Union

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

    for dmg_type in valid_types:
        # Includes abreviation support for damge types (spelling bludgeoning is hard!)
        if input_type in (dmg_type, dmg_type[:2]):
            return dmg_type
    return False