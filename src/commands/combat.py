"""Combat Commands"""

import argparse
import os

from discord import Embed
from discord.ext.commands import Bot, Cog, Context, command

from utils.argparse_utils import ArgParseError
from utils.combat.args import CombatArgs, get_combat_args
from utils.combat.client import CombatClient
from utils.embed import create_error_embed
from utils.logging import get_logger

LOGGER = get_logger(os.path.basename(__file__))


class Combat(Cog):
    """Cog defining commands related to combat"""

    def __init__(self: "Combat", bot: Bot) -> None:
        """Init Cog

        Args:
            bot (`Bot`): Discord Bot object
        """
        self.bot = bot

    @command(name="combat", help="Handle combat related tasks")
    async def handle_combat(self: "Combat", ctx: Context, *args) -> None:  # noqa: C901, PLR0912
        """Begin a new combat encounter, or load a saved encounter

        Args:
            ctx (`Context`): Message context object from Discord
        """
        """
        if not args or args[0] not in SUB_COMMANDS:
            response = f"Please specify a valid subcommand. Options: {SUB_COMMANDS}"
            await ctx.send(response)
            return
        """
        try:
            no_em_dash = [arg.replace("—", "--") for arg in args]
            combat_args = get_combat_args(*no_em_dash)
        except (ArgParseError, argparse.ArgumentError, argparse.ArgumentTypeError) as error:
            LOGGER.exception(error, exc_info=error)
            embed = create_error_embed(error, multiline=True)
            await ctx.send(embed=embed)
            return

        combat_client = CombatClient()

        if combat_args.sub_command == "begin":
            await begin_combat(ctx, combat_client, combat_args.combat_id)
        elif combat_args.sub_command == "save":
            await save_combat(ctx, combat_client, combat_args.combat_id)
        elif combat_args.sub_command == "load":
            await load_combat(ctx, combat_client, combat_args.combat_id)
        elif combat_args.sub_command == "clear":
            await clear_combat(ctx, combat_client)
        elif combat_args.sub_command == "show":
            await show_combat(ctx, combat_client, combat_args)
        elif combat_args.sub_command == "list":
            await list_encounters(ctx, combat_client)
        elif combat_args.sub_command == "add":
            await add_character(ctx, combat_client, combat_args)
        elif combat_args.sub_command == "madd":
            await add_monster(ctx, combat_client, combat_args)
        elif combat_args.sub_command == "update":
            await update_character(ctx, combat_client, combat_args)
        elif combat_args.sub_command == "rm":
            await remove_character(ctx, combat_client, combat_args)
        else:
            response = "should not have gotten here...."
            await ctx.send(response)


async def begin_combat(
    ctx: Context,
    combat_client: CombatClient,
    combat_id: str = None,
) -> None:
    """Begin a new combat encounter, or load a saved encounter

    Args:
        ctx (`Context`): Message context object from Discord
        combat_client (`CombatClient`): Combat client
        combat_id (`str`, optional): ID of combat to load. If ommitted, a new encounter will be started. Defaults to `None`.
    """
    response = await combat_client.begin(combat_id)
    if isinstance(response, Embed):
        await ctx.send(embed=response)
    else:
        response = "Something went wrong! Could not begin encounter..."
        await ctx.send(response)


async def save_combat(
    ctx: Context,
    combat_client: CombatClient,
    combat_id: str,
) -> None:
    """Save current combat encounter

    Args:
        ctx (`Context`): Message context object from Discord
        combat_client (`CombatClient`): Combat client
        combat_id (`str`): ID of combat to save
    """
    combat_path = await combat_client.save(combat_id)
    response = f"Saved combat to `{combat_path}`"
    await ctx.send(response)


async def load_combat(
    ctx: Context,
    combat_client: CombatClient,
    combat_id: str = None,
) -> None:
    """Load a saved combat encounter

    Args:
        ctx (`Context`): Message context object from Discord
        combat_client (`CombatClient`): Combat client
        combat_id (`str`, optional): ID of combat to load. If ommitted, saved encounters will be listed. Defaults to `None`.
    """
    response = await combat_client.load(combat_id)
    if isinstance(response, Embed):
        await ctx.send(embed=response)
    else:
        response = "Something went wrong! Could not load encounter..."
        await ctx.send(response)


async def clear_combat(
    ctx: Context,
    combat_client: CombatClient,
) -> None:
    """Clear combat encounter

    Args:
        ctx (`Context`): Message context object from Discord
        combat_client (`CombatClient`): Combat client
    """
    await combat_client.clear()
    response = "Cleared currrent combat"
    await ctx.send(response)


async def show_combat(ctx: Context, combat_client: CombatClient, combat_args: CombatArgs) -> None:
    """Show the combat encounter.

    Args:
        ctx (`Context`): Message context object from Discord
        combat_client (`CombatClient`): Combat client
    """
    response = await combat_client.show(combat_args.as_text)
    if isinstance(response, Embed):
        await ctx.send(embed=response)
    else:
        response = "Something went wrong! Could not generate encounter embed..."
        await ctx.send(response)


async def list_encounters(
    ctx: Context,
    combat_client: CombatClient,
) -> None:
    """List the saved combat encounters.

    Args:
        ctx (`Context`): Message context object from Discord
        combat_client (`CombatClient`): Combat client
    """
    response = combat_client.list()
    if isinstance(response, Embed):
        await ctx.send(embed=response)
    else:
        response = "Something went wrong! Could not list encounters..."
        await ctx.send(response)


async def add_character(ctx: Context, combat_client: CombatClient, combat_args: CombatArgs) -> None:
    """Add a player character to the encounter

    Args:
        ctx (`Context`): Message context object from Discord
        combat_client (`CombatClient`): Combat client
        combat_args (`CombatArgs`): Command arguments with character data
    """
    char_dict = combat_args.__dict__
    # Remove the sub_command item from the dict
    del char_dict["sub_command"]
    await combat_client.add(char_dict)
    response = f"Added PC `{combat_args.name}`"
    await ctx.send(response)


async def add_monster(ctx: Context, combat_client: CombatClient, combat_args: CombatArgs) -> None:
    """Add a non-player character to the encounter

    Args:
        ctx (`Context`): Message context object from Discord
        combat_client (`CombatClient`): Combat client
        combat_args (`CombatArgs`): Command arguments with character data
    """
    char_dict = combat_args.__dict__
    # Remove the sub_command item from the dict
    del char_dict["sub_command"]
    await combat_client.madd(char_dict)
    response = f"Added NPC `{combat_args.name}`"
    await ctx.send(response)


async def update_character(ctx: Context, combat_client: CombatClient, combat_args: CombatArgs) -> None:
    """Update an existing character

    Args:
        ctx (`Context`): Message context object from Discord
        combat_client (`CombatClient`): Combat client
        combat_args (`CombatArgs`): Command arguments with character data
    """
    char_dict = combat_args.__dict__
    # Remove the sub_command item from the dict
    del char_dict["sub_command"]
    response = await combat_client.update(char_dict)
    await ctx.send(response)


async def remove_character(ctx: Context, combat_client: CombatClient, combat_args: CombatArgs) -> None:
    """Remove a character from the encounter

    Args:
        ctx (`Context`): Message context object from Discord
        combat_client (`CombatClient`): Combat client
        combat_args (`CombatArgs`): Command arguments with character data
    """
    response = await combat_client.remove(combat_args.name)
    await ctx.send(response)


async def setup(bot: Bot) -> None:
    """Setup Cog

    Args:
        bot (`Bot`): Discord Bot object
    """
    await bot.add_cog(Combat(bot))
