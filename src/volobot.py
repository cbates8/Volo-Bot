"""Event and command definitions for VoloBot: The best D&D Discord bot in the multiverse!
Author: Casey Bates
GitHub: https://github.com/cbates8/Volo-Bot
"""

import os

from discord import Intents
from discord.ext.commands import Bot

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
INITIAL_EXTENSIONS = ["commands.event", "commands.crit", "commands.dev", "commands.inventory", "commands.misc", "commands.spell"]


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


###############
### RUN BOT ###
###############


if __name__ == "__main__":
    bot = VoloBot(extensions=INITIAL_EXTENSIONS, command_prefix=COMMAND_PREFIX, description=DESCRIPTION, intents=INTENTS)
    bot.run(TOKEN, log_handler=None)
