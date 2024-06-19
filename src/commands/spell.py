"""Spell Commands"""

from urllib.error import HTTPError

from discord.ext.commands import Bot, Cog, Context, command, parameter

from src.constants.paths import SPELLS_PATH
from src.utils.embed import dict_to_embed
from src.utils.spell import get_ddb_spell
from src.utils.utils import load_json


class Spell(Cog):

    def __init__(self: "Spell", bot: Bot):
        self.bot = bot

    @command(name="spell", help="Search spell descriptions")
    async def send_spell_description(
        self: "Spell",
        ctx: Context,
        spell_name: str = parameter(description="The name of the spell to search for"),
        source: str = parameter(default="all", description="Source to get spell info from ('local' | 'web' )"),
    ) -> None:
        """Search for a spell and return its description

        Args:
            ctx (`Context`): Message context object from Discord
            spell_name (`str`): The name of the spell to search for
            source (`str`, optional): The source to check for spell info. Defaults to 'all'
        """
        source = source.lower()
        if source not in ["all", "local", "web"]:
            response = f"**Error:** Invalid Source '{source}'\nMust be one of 'local' or 'web'"
            await ctx.send(response)
            return

        if source != "web":
            # Search local spell file for information
            known_spells = load_json(SPELLS_PATH)

            for spell in known_spells:
                if spell_name.lower() == spell.lower():
                    embed = dict_to_embed(spell, known_spells[spell])
                    await ctx.send(embed=embed)
                    return
            if source == "local":
                response = f"**Error:** Cannot find spell '{spell_name}'"
                await ctx.send(response)

        if source == "all":
            # If spell can't be found locally, scrape D&D Beyond
            response = f"Searching D&D Beyond for spell '{spell_name}'"
            await ctx.send(response)

        if source != "local":
            try:
                embed = get_ddb_spell(spell_name)
                await ctx.send(embed=embed)
            except HTTPError:
                response = f"**Error:** Cannot find spell '{spell_name}'"
                await ctx.send(response)


async def setup(bot: Bot):
    await bot.add_cog(Spell(bot))
