"""Event and command definitions for VoloBot: the worlds best D&D Discord bot!
Author: Casey Bates
Repo: https://github.com/cbates8/Volo-Bot
"""
from csv import DictReader
import os
import random
from typing import Any
from discord import Activity, ActivityType, Embed, File, Game, Intents, Message
from discord.ext.commands import Bot, Context, parameter
from discord.utils import get
from dotenv import load_dotenv
from quotes import QUOTES
from urllib.error import HTTPError
from utils import (
    create_error_embed,
    dict_to_embed,
    get_ddb_spell,
    load_json,
    print_error,
    validate_crit_percentage,
    validate_damage_type,
    write_json,
)

#################
### BOT SETUP ###
#################

# Parse .env file
load_dotenv()
# Get DISCORD_TOKEN from token specified in the .env file
TOKEN = os.getenv("DISCORD_TOKEN")
# Get DISCORD_GUILD from guild ID specified in the .env file
GUILD = os.getenv("DISCORD_GUILD")

# Define intents for the bot
INTENTS = Intents.default()
INTENTS.message_content = True  # pylint: disable=assigning-non-slot

DESCRIPTION = """A Dungeons and Dragons bot based on Volothamp Geddarm.

Capable of rolling dice, checking critical hit tables, and more!"""

# command_prefix= defines the bot's command prefix (string)
# description= will add a description to the !help menu (string)
bot = Bot(command_prefix="!", description=DESCRIPTION, intents=INTENTS)


##################
### BOT EVENTS ###
##################


@bot.event
async def on_ready() -> None:
    """On ready, bot will print to the console confirming its connection to discord, as well as the guild specified in the .env file"""
    print(f"{bot.user.name} has connected to Discord!")

    guild = get(bot.guilds, name=GUILD)
    print(f"{bot.user.name} is connected to the following guild:\n{guild.name}(id: {guild.id})")
    # set activity status to "Playing Dungeons and Dragons"
    # await bot.change_presence(activity=discord.CustomActivity(name="Reading \'Volo\'s Guide to Monsters\'", emoji=None, type=discord.ActivityType.custom))
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
    await bot.process_commands(
        message
    )  # Without this line, the following commands will not work, and only this on_message event will run


@bot.event
async def on_command_error(ctx: Context, error: Any) -> None:
    """Send error messages to context rather than printing to console

    Args:
        ctx (`Context`): Message context object from Discord
        error (`Any`): The error encountered in the program. This will either be a UserInputError or some other error thrown by the program
    """
    print_error(error)

    embed = create_error_embed(error)
    await ctx.send(embed=embed)


####################
### BOT COMMANDS ###
####################


@bot.command(name="crit", help="Search the critical hit table")
async def send_crit_outcome(
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
        with open("Critical_Hit_Table.csv", mode="r", encoding="utf8") as csvfile:
            csvreader = DictReader(csvfile)
            roll_values = csvreader.fieldnames[0]
            valid_dmg_types = csvreader.fieldnames[1:]

            dmg_type = validate_damage_type(valid_dmg_types, dmg_type)
            if dmg_type:
                for row in csvreader:
                    # Uses 'row' as the dictionary identifier and finds the value assigned to key 'dmg_type'
                    if int(row[roll_values]) == crit_percentage:
                        response = row[dmg_type]
                        break
            else:
                # using chr(10) as newline, because f-string doesn't support \n in expression part
                response = f"**Error:** Invalid Damage Type\nSupported types: ```{chr(10).join(valid_dmg_types)}```"
    else:
        response = "**Error:** Invalid Percentage Roll\nMust be value from 1-100"
    await ctx.send(response)


@bot.command(name="spell", help="Search spell definitions")
async def send_spell_description(
    ctx: Context, spell_name: str = parameter(description="The name of the spell to search for")
) -> None:
    """Search for a spell and return its description

    Args:
        ctx (`Context`): Message context object from Discord
        spell_name (`str`): The name of the spell to search for
    """

    known_spells = load_json("spells.json")

    embed = Embed(title=f"Can't find spell '{spell_name}'")
    for spell in known_spells:
        if spell_name.lower() == spell.lower():
            embed = dict_to_embed(spell, known_spells[spell])
            break
    await ctx.send(embed=embed)


######################
# Test spell command #
######################


@bot.command(name="test_spell")
async def test_spell(ctx, spell_name):
    try:
        embed = get_ddb_spell(spell_name)
        await ctx.send(embed=embed)
    except HTTPError:
        response = f"**Error:** Cannot find spell '{spell_name}'"
        await ctx.send(response)


######################
# Test spell command #
######################


@bot.command(name="roll", help="Roll virtual dice")
async def roll_dice(
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


@bot.command(name="set_activity", help="Set the bot's activity")
async def set_activity(
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
        await bot.change_presence(
            activity=Game(name=activity_name)
        )  # sets activity to 'Playing activity_name'
    elif activity_type.lower() == "listening":
        await bot.change_presence(
            activity=Activity(type=ActivityType.listening, name=activity_name)
        )  # sets activity to "Listening to activity_name"
    elif activity_type.lower() == "watching":
        await bot.change_presence(
            activity=Activity(type=ActivityType.watching, name=activity_name)
        )  # sets activity to "Watching activity_name"
    else:
        await ctx.send(
            "Activity not supported. Supported Activities: Playing, Listening, Watching"
        )  # Sends a list of supported activities if one isn't given


@bot.command(name="meme", help="Dank Me Me")
async def send_meme(ctx: Context):
    """Sends a meme to context

    Args:
        ctx (`Context`): Message context object from Discord
    """
    random_meme = random.choice(os.listdir("Memes"))  # choose a random file from the "Memes" folder
    while (
        random_meme == ".DS_Store"
    ):  # If .DS_Store is selected at random, continue choosing until the selected file is NOT .DS_Store
        random_meme = random.choice(os.listdir("Memes"))
    await ctx.send(file=File(f"Memes/{random_meme}"))


@bot.command(name="ping", help="Ping Volobot")
async def send_ping_response(ctx: Context) -> None:
    """Send the estimated ping of the requesting user

    Args:
        ctx (`Context`): Message context object from Discord
    """
    embed = Embed(title="Pong!")
    response = await ctx.send(embed=embed)
    ping = (
        response.created_at - ctx.message.created_at
    ).total_seconds() * 1000  # Calculate the time difference between ping request and pong response
    embed.add_field(name=":ping_pong:", value=f"{int(ping)} ms")  # Add calculated ping to the embed
    await response.edit(embed=embed)  # edit response to include calculated ping (ms)


@bot.command(name="bag", help="Check the party's inventory")
async def check_inventory(
    ctx: Context,
    item: str = parameter(
        default=None,
        description=" The name of the inventory item to list. If ommitted, entire inventory will be listed",
    ),
) -> None:
    """Displays the contents of inventory.json

    Args:
        ctx (`Context`): Message context object from Discord
        item (`str`, optional): The name of the inventory item to list. If ommitted, entire inventory will be listed. Defaults to `None`.
    """
    inventory = load_json("inventory.json")

    if item is None:
        embed = dict_to_embed("Inventory", inventory)
    else:
        embed = dict_to_embed(item, inventory[item])

    await ctx.send(embed=embed)


@bot.command(name="store", help="Store items in the party's inventory")
async def store_inventory(
    ctx: Context,
    item: str = parameter(description="The name of the item to store"),
    description: str = parameter(default=None, description="A description of the stored item"),
    quantity: int = parameter(default=1, description="The quantity of the item to store"),
) -> None:
    """Store items in inventory (write to inventory.json)

    Args:
        ctx (`Context`): Message context object from Discord
        item (`str`): The name of the item to store
        description (`str`, optional): A description of the stored item. Defaults to `None`.
        quantity (`int`, optional): The quantity of the item to store. Defaults to `1`.
    """
    inventory = load_json("inventory.json")

    if item in inventory.keys():
        inventory[item]["quantity"] += quantity
        if description is not None:
            inventory[item]["description"] = description
    else:
        inventory[item] = {"description": description, "quantity": quantity}

    write_json("inventory.json", inventory)

    response = f"Added {quantity} {item} to your inventory."

    await ctx.send(response)


@bot.command(name="remove", help="Remove items from the party's inventory")
async def remove_inventory(
    ctx: Context,
    item: str = parameter(description="The name of the item to remove"),
    quantity: int = parameter(default=None, description="The quantity of the item to remove"),
):
    """Remove items from inventory.json

    Args:
        ctx (`Context`): Message context object from Discord
        item (`str`): Item to remove from the inventory
        quantity (`int`, optional): The quantity of items to remove. Defaults to `None` (Removes all items).
    """
    inventory = load_json("inventory.json")

    if quantity is None or quantity >= inventory[item]["quantity"]:
        del inventory[item]
    else:
        inventory[item]["quantity"] -= quantity

    write_json("inventory.json", inventory)

    response = f"Removed {'all' if quantity is None else quantity} {item} from your inventory."

    await ctx.send(response)


###############
### RUN BOT ###
###############

bot.run(TOKEN)
