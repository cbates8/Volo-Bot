"""Rule Commands"""

from discord import Embed
from discord.ext.commands import Bot, Cog, Context, command, parameter

from utils.rules import get_rule


class Rule(Cog):
    """Cog defining commands related to rule lookup"""

    def __init__(self: "Rule", bot: Bot) -> None:
        """Init Cog

        Args:
            bot (`Bot`): Discord Bot object
        """
        self.bot = bot

    @command(name="rule", help="Search rule descriptions")
    async def send_spell_description(
        self: "Rule",
        ctx: Context,
        rule_name: str = parameter(description="The name of the rule to search for"),
    ) -> None:
        """Search for a rule and return its description

        Args:
            ctx (`Context`): Message context object from Discord
            rule_name (`str`): The name of the rule to search for
        """
        response = await get_rule(rule_name)
        if isinstance(response, Embed):
            await ctx.send(embed=response)
        else:
            await ctx.send(response)


async def setup(bot: Bot) -> None:
    """Setup Cog

    Args:
        bot (`Bot`): Discord Bot object
    """
    await bot.add_cog(Rule(bot))
