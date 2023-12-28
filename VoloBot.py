"""Event and command definitions for VoloBot: the worlds best D&D Discord bot!
Author: Casey Bates
GitHub: https://github.com/cbates8/Volo-Bot
"""
import os
import random
from csv import DictReader
from typing import Any
from urllib.error import HTTPError
from discord import Activity, ActivityType, Embed, File, Game, Intents, Message
from discord.ext.commands import Bot, Context, parameter
from dotenv import load_dotenv
from quotes import QUOTES
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

# Define intents for the bot
INTENTS = Intents.default()
INTENTS.message_content = True

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
    print(f"{bot.user.name} is connected to the following guilds:")
    for guild in bot.guilds:
        print(f"\t{guild.name} (id: {guild.id})")
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
    # Without this line, the following commands will not work, and only this on_message event will run
    await bot.process_commands(message)


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


@bot.command(name="fumble", help="Search the critical miss table")
async def send_fumble_outcome(
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
        with open("Fumble_Table.csv", mode="r", encoding="utf8") as csvfile:
            csvreader = DictReader(csvfile)
            roll_values = csvreader.fieldnames[0]
            fumble_effects = csvreader.fieldnames[1]

            for row in csvreader:
                # Uses 'row' as the dictionary identifier and finds the value assigned to key 'fumble_effects'
                if int(row[roll_values]) == fumble_percentage:
                    response = row[fumble_effects]
                    break
    else:
        response = "**Error:** Invalid Percentage Roll\nMust be value from 1-100"
    await ctx.send(response)


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
                response = f"**Error:** Invalid Damage Type\nSupported types: ```\n{chr(10).join(valid_dmg_types)}```"
    else:
        response = "**Error:** Invalid Percentage Roll\nMust be value from 1-100"
    await ctx.send(response)


@bot.command(name="spell", help="Search spell descriptions")
async def send_spell_description(
    ctx: Context,
    spell_name: str = parameter(description="The name of the spell to search for"),
    source: str = parameter(
        default="all", description="Source to get spell info from ('local' | 'web' )"
    ),
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
        known_spells = load_json("spells.json")

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
        # sets activity to 'Playing activity_name'
        await bot.change_presence(activity=Game(name=activity_name))
    elif activity_type.lower() == "listening":
        # sets activity to "Listening to activity_name"
        await bot.change_presence(
            activity=Activity(type=ActivityType.listening, name=activity_name)
        )
    elif activity_type.lower() == "watching":
        # sets activity to "Watching activity_name"
        await bot.change_presence(activity=Activity(type=ActivityType.watching, name=activity_name))
    else:
        # Sends a list of supported activities if one isn't given
        await ctx.send("Activity not supported. Supported Activities: Playing, Listening, Watching")


@bot.command(name="meme", help="Dank Me Me")
async def send_meme(ctx: Context):
    """Sends a meme to context

    Args:
        ctx (`Context`): Message context object from Discord
    """
    random_meme = random.choice(os.listdir("Memes"))  # choose a random file from the "Memes" folder
    # If .DS_Store is selected at random, continue choosing until the selected file is NOT .DS_Store
    while random_meme == ".DS_Store":
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
    # Calculate the time difference between ping request and pong response
    ping = (response.created_at - ctx.message.created_at).total_seconds() * 1000
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
        quantity (`int`, optional): The quantity of the item to store. Defaults to '1'.
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
