"""Critical Hit/Miss Commands"""

import aiofiles
from aiocsv import AsyncDictReader
from discord.ext.commands import Bot, Cog, Context, command, parameter

from src.constants.paths import CRIT_TABLE_PATH, FUMBLE_TABLE_PATH
from src.utils.utils import validate_crit_percentage, validate_damage_type


class Crit(Cog):
    """Cog defining commands related to critical hits and misses"""

    def __init__(self: "Crit", bot: Bot) -> None:
        """Init Cog

        Args:
            bot (`Bot`): Discord Bot object
        """
        self.bot = bot

    @command(name="crit", help="Search the critical hit table")
    async def send_crit_outcome(
        self: "Crit",
        ctx: Context,
        crit_percentage: int = parameter(description="Percentage representing critical hit severity"),
        dmg_type: str = parameter(description="Type of damage being inflicted"),
    ) -> None:
        """Search the provided csv of the crititcal hit table using the user's inputed percentage and damage type. Reply with the resulting effect

        Args:
            ctx (`Context`): Message context object from Discord
            crit_percentage (`int`): Percentage representing critical hit severity
            dmg_type (`str`): Type of damage being inflicted
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
        await ctx.send(response)

    @command(name="fumble", help="Search the critical miss table")
    async def send_fumble_outcome(
        self: "Crit",
        ctx: Context,
        fumble_percentage: int = parameter(description="Percentage representing critical miss severity"),
    ) -> None:
        """Search the provided csv of the crititcal miss table using the user's inputed percentage. Reply with the resulting effect

        Args:
            ctx (`Context`): Message context object from Discord
            fumble_percentage (`int`): Percentage representing critical miss severity
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
        await ctx.send(response)


async def setup(bot: Bot) -> None:
    """Setup Cog

    Args:
        bot (`Bot`): Discord Bot object
    """
    await bot.add_cog(Crit(bot))
