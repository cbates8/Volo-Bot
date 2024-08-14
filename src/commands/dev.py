"""Developer Commands"""

from discord import Activity, ActivityType, Game
from discord.ext.commands import Bot, Cog, Context, command, is_owner, parameter

from src.utils.utils import get_cog_path


class Dev(Cog):
    """Cog defining developer commands.
    These commands are hidden and will only be available to users with elevated permissions
    """

    def __init__(self: "Dev", bot: Bot) -> None:
        """Init Cog

        Args:
            bot (`Bot`): Discord Bot object
        """
        self.bot = bot

    @command(name="load", hidden=True)
    @is_owner()
    async def load_cog(self: "Dev", ctx: Context, *, cog: str) -> None:
        """Command which Loads a Module

        Args:
            ctx (`Context`): Message context object from Discord
            cog (`str`): Name of the cog to unload
        """
        path = get_cog_path(cog)

        try:
            await self.bot.load_extension(path)
        except Exception as e:
            await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
        else:
            await ctx.send("**`SUCCESS`**")

    @command(name="unload", hidden=True)
    @is_owner()
    async def unload_cog(self: "Dev", ctx: Context, *, cog: str) -> None:
        """Command which Unloads a Module

        Args:
            ctx (`Context`): Message context object from Discord
            cog (`str`): Name of the cog to unload
        """
        path = get_cog_path(cog)

        try:
            await self.bot.unload_extension(path)
        except Exception as e:
            await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
        else:
            await ctx.send("**`SUCCESS`**")

    @command(name="reload", hidden=True)
    @is_owner()
    async def reload_cog(self: "Dev", ctx: Context, *, cog: str) -> None:
        """Command which Reloads a Module

        Args:
            ctx (`Context`): Message context object from Discord
            cog (`str`): Name of the cog to unload
        """
        path = get_cog_path(cog)

        try:
            await self.bot.unload_extension(path)
            await self.bot.load_extension(path)
        except Exception as e:
            await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
        else:
            await ctx.send("**`SUCCESS`**")

    @command(name="set_activity", help="Set the bot's activity", hidden=True)
    @is_owner()
    async def set_activity(
        self: "Dev",
        ctx: Context,
        activity_type: str = parameter(description="Type of activity to be displayed (e.g. 'Playing')"),
        activity_name: str = parameter(description="Description of activity to be displayed"),
    ) -> None:
        """Set the bot's Discord activity status

        Args:
            ctx (`Context`): Message context object from Discord
            activity_type (`str`): Type of activity to be displayed (e.g. "Playing", "Listening", "Watching")
            activity_name (`str`): Description of activity to be displayed (e.g. "Playing [activity_name]")
        """
        if activity_type.lower() == "playing":
            # sets activity to 'Playing activity_name'
            await self.bot.change_presence(activity=Game(name=activity_name))
        elif activity_type.lower() == "listening":
            # sets activity to "Listening to activity_name"
            await self.bot.change_presence(activity=Activity(type=ActivityType.listening, name=activity_name))
        elif activity_type.lower() == "watching":
            # sets activity to "Watching activity_name"
            await self.bot.change_presence(activity=Activity(type=ActivityType.watching, name=activity_name))
        else:
            # Sends a list of supported activities if one isn't given
            await ctx.send("Activity not supported. Supported Activities: Playing, Listening, Watching")


async def setup(bot: Bot) -> None:
    """Setup Cog

    Args:
        bot (`Bot`): Discord Bot object
    """
    await bot.add_cog(Dev(bot))
