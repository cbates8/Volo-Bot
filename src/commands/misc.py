"""Misc Commands"""

import os
import random

from discord import Embed, File
from discord.ext.commands import Bot, Cog, Context, command, parameter


class Misc(Cog):
    def __init__(self: "Misc", bot: Bot):
        self.bot = bot

    @command(name="roll", help="Roll virtual dice")
    async def roll_dice(
        self: "Misc",
        ctx: Context,
        number_of_dice: int = parameter(description="The number of dice to be rolled"),
        number_of_sides: int = parameter(description="How many sides each rolled die should have"),
    ) -> None:
        """Simulate rolling of dice

        Args:
            ctx (`Context`): Message context object from Discord
            number_of_dice (`int`): The number of dice to be rolled
            number_of_sides (`int`): How many sides each rolled die should have
        """
        # Chooses a random int between 1 and the given number of sides
        # Repeats as many times as number_of_dice
        dice = [str(random.choice(range(1, number_of_sides + 1))) for _ in range(number_of_dice)]
        await ctx.send(", ".join(dice))

    @command(name="meme", help="Dank Me Me")
    async def send_meme(self: "Misc", ctx: Context):
        """Sends a meme to context

        Args:
            ctx (`Context`): Message context object from Discord
        """
        random_meme = random.choice(os.listdir("memes"))  # choose a random file from the "memes" folder
        # If .DS_Store is selected at random, continue choosing until the selected file is NOT .DS_Store
        while random_meme == ".DS_Store":
            random_meme = random.choice(os.listdir("memes"))
        await ctx.send(file=File(f"memes/{random_meme}"))

    @command(name="ping", help="Ping Volobot")
    async def send_ping(self: "Misc", ctx: Context) -> None:
        """Send the estimated ping of the requesting user

        Args:
            ctx (`Context`): Message context object from Discord
        """
        embed = Embed(title="Pong!")
        response = await ctx.send(embed=embed)
        # Calculate the time difference between ping request and pong response
        ping = (response.created_at - ctx.message.created_at).total_seconds() * 1000
        embed.add_field(name=":ping_pong:", value=f"{int(ping)} ms")  # Add calculated ping to the embed
        await response.edit(embed=embed)  # edit response to include calculated ping (ms)


async def setup(bot: Bot):
    await bot.add_cog(Misc(bot))
