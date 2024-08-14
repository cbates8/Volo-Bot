"""Event and command definitions for VoloBot: The best D&D Discord bot in the multiverse!
Author: Casey Bates
GitHub: https://github.com/cbates8/Volo-Bot
"""

import os
import random
from typing import Any

from discord import Game, Intents, Message
from discord.ext.commands import Bot, Context

from constants.quotes import QUOTES
from utils.embed import create_error_embed
from utils.logging import get_logger

LOGGER = get_logger(os.path.basename(__file__))

#################
### BOT SETUP ###
#################

# Get DISCORD_TOKEN from env var
TOKEN = os.getenv("DISCORD_TOKEN")

# Define command prefix
COMMAND_PREFIX = "!"

# Define intents for the bot
INTENTS = Intents.default()
INTENTS.message_content = True

# Add a description to the !help menu
DESCRIPTION = """A Dungeons and Dragons bot based on Volothamp Geddarm.

Capable of rolling dice, checking critical hit tables, and more!"""

# Cogs the bot should start with
INITIAL_EXTENSIONS = ["commands.crit", "commands.dev", "commands.inventory", "commands.misc", "commands.spell"]


class VoloBot(Bot):
    """VoloBot, a D&D Discord Bot"""

    def __init__(self: "VoloBot", extensions: str, **kwargs) -> None:
        """Initialize Volobot, pass kwargs to Bot constructor

        Args:
            extensions (`str`): List of extensions (cogs) to load
        """
        super().__init__(**kwargs)  # Pass kwargs to Bot constructor
        self.initial_extensions = extensions

    async def setup_hook(self: "VoloBot") -> None:
        """A coroutine to be called to setup the bot.

        In our case, that means loading our initial extensions (cogs).

        Will be executed after the bot is logged in but before it has connected to the Websocket.
        This is only called once, in login, and will be called before any events are dispatched,
        making it a better solution than doing such setup in the `~discord.on_ready` event.

        """
        for extension in self.initial_extensions:
            await bot.load_extension(extension)


bot = VoloBot(extensions=INITIAL_EXTENSIONS, command_prefix=COMMAND_PREFIX, description=DESCRIPTION, intents=INTENTS)


##################
### BOT EVENTS ###
##################


@bot.event
async def on_ready() -> None:
    """On ready, bot will log to the console confirming its connection to discord, as well as any guilds it has been added to"""
    LOGGER.info("%s has connected to Discord!", bot.user.name)
    LOGGER.info("%s is connected to the following guilds:", bot.user.name)
    for guild in bot.guilds:
        LOGGER.info("\t- %s (id: %s)", guild.name, guild.id)
    # await bot.change_presence(activity=discord.CustomActivity(name="Reading \'Volo\'s Guide to Monsters\'", emoji=None, type=discord.ActivityType.custom))
    # set activity status to "Playing Dungeons and Dragons"
    await bot.change_presence(activity=Game(name="Dungeons and Dragons"))


@bot.event
async def on_message(message: Message) -> None:
    """When seeing a message containing 'volo', bot will reply with a random quote from the list stored in volo_quotes

    Args:
        message (`Message`): A Message object from Discord
    """
    # checks if the bot was the one to send the message. If so, breaks out of function to avoid a continuous reply to itself
    if message.author == bot.user:
        return
    # If any version of the string 'volo' appears in a message, choose a random quote and send it to the channel
    if "volo" in message.content.lower():
        response = random.choice(QUOTES)
        await message.channel.send(response)
    # Without this line, the following commands will not work. Only this on_message event will run
    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx: Context, error: Any) -> None:
    """Send error messages to context in addition to logging

    Args:
        ctx (`Context`): Message context object from Discord
        error (`Any`): The error encountered in the program. This will either be a UserInputError or some other error thrown by the program
    """
    LOGGER.exception(error, exc_info=error)
    embed = create_error_embed(error)
    await ctx.send(embed=embed)


###############
### RUN BOT ###
###############

bot.run(TOKEN, log_handler=None)
