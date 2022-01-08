#####################################
#####################################
# VoloBot.py
# Author: Casey Bates
# https://github.com/cbates8/Volo-Bot
#####################################
#####################################
import os
import random
import discord
import traceback
import json
import helpers
from csv import DictReader
from dotenv import load_dotenv
from discord.ext import commands

#################
### BOT SETUP ###
#################

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') #gets DISCORD_TOKEN from token specified in the .env file
GUILD = os.getenv('DISCORD_GUILD') #gets DISCORD_GUILD from guild ID specified in the .env file

description = '''A Dungeons and Dragons bot based on Volothamp Geddarm.

Capable of rolling dice, checking critical hit tables, and more!'''

#command_prefix= defines the bot's command prefix (string)
#description= will add a description to the !help menu (string)
bot = commands.Bot(command_prefix='!', description=description)


##################
### BOT EVENTS ###
##################

@bot.event
async def on_ready():
    """
    On ready, bot will print to the console confirming its connection to discord, as well as the guild specified in the .env file
    """

    print(f'{bot.user.name} has connected to Discord!')

    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f'{bot.user.name} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    #set activity status to "Playing Dungeons and Dragons"
    #await bot.change_presence(activity=discord.CustomActivity(name="Reading \'Volo\'s Guide to Monsters\'", emoji=None, type=discord.ActivityType.custom))
    await bot.change_presence(activity=discord.Game(name="Dungeons and Dragons"))

###################
###################
@bot.event
async def on_message(message):
    """
    When seeing a message containing 'volo', bot will reply with a random quote from the list stored in volo_quotes

    Parameters
    ----------
    message : `discord.Message`
        Message object from Discord
    """

    #checks if the bot was the one to send the message. If so, breaks out of function to avoid a continuous reply to itself
    if message.author == bot.user:
        return

    ### TODO: Import quotes from seperate file instead of hard-coded list?
    volo_quotes = [
        # Taken from the commentary in his fantastical dissertation: 'Volo's Guide to Monsters'
        'Volothamp Geddarm at your service.',
        'When beholders dream of beholders, that\'s when the trouble starts',
        'A beholder always has several backup plans ready. When dealing with one, I have three plans of my own; run, hide, and distract. Rival adventurers are always a good distraction, Rival beholders are the best one.',
        'Kobolds are a lot less cute when they learn how to cast fireballs.',
        'I wonder what a mind flayer\'s brain tastes like.',
        '\'Grungs\' are sentient, poisonous frogs that live in trees. Truly, the gods hate us.',
        'Damn eel-spiders want to enslave us all! And no, they don\'t taste good.',
        'Sometimes you eat the worm -- and sometimes the worm eats you.',
        'If you say the name Raxivort three times while gazing at your reflection in a mirror, xvarts will visit you in the dead of night and steal a cherished trinket.',
    ]

    #If any version of the string 'volo' appears in a message, choose a random quote and send it to the channel
    if 'volo' in message.content.lower():
        response = random.choice(volo_quotes)
        await message.channel.send(response)
    await bot.process_commands(message) #Without this line, the following commands will not work, and only this on_message event will run

###################
###################
@bot.event
async def on_command_error(ctx, error):
    """
    Send error messages to context rather than print to console

    Parameters
    ----------
    ctx : `discord.ext.commands.Context`
        Message context object from Discord

    error : `UserInputError`
        Exception to be sent to the channel context by the bot
    """

    embed = discord.Embed(title="I've encountered an error:")
    if isinstance(error, commands.BadArgument):
        embed.add_field(name="Bad Argument", value="An argument was passed as an incorrect type.", inline=False)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed.add_field(name="Missing Required Argument", value="Send '!help <command>' to learn more about a command.", inline=False)
    elif isinstance(error, commands.TooManyArguments):
        embed.add_field(name="Too Many Arguments", value="Send '!help <command>' to learn more about a command.", inline=False)
    else:
        embed.add_field(name="Exception Thrown", value='Yikes!', inline=False)
    embed.add_field(name="Error Text:", value=f'`{error}`', inline=False)
    print(f'Error: {error}\n-----\nTraceback: {traceback.print_exc}\n\n') ##TODO: Implement correct traceback
    await ctx.send(embed=embed)



####################
### BOT COMMANDS ###
####################

@bot.command(name='crit', help='Search the critical hit table')
async def crit_roll(ctx, percentage: int, damage_type: str):
    """
    Search the provided csv of the crititcal hit table using the user's inputed percentage and damage type. Reply with the resulting effect

    Parameters
    ----------
    ctx : `discord.ext.commands.Context`
        Message context object from Discord

    percentage : `int`
        Percentage representing critical hit severity

    damage_type : `str`
        Type of damage being inflicted
    """
    damage_type = damage_type.lower()

    #Opens 'Critical Hit Table.csv' and treats it as a dictionary. First row treated as keys, with following rows each being its own set of values for those keys
    with open('Critical Hit Table.csv', mode='r') as csvfile:
        csvreader = DictReader(csvfile)
        line_count = 1
        
        valid_response = False
        for header in csvreader.fieldnames[1:]:
            if damage_type == header or damage_type == header[:2]: # Includes abreviation support for damge types (spelling bludgeoning is hard!)
                damage_type = header
                valid_response = True
                break
        
        #if percentage not in range(1, 101):
        response = 'Error: Invalid Percentage Roll\nMust be value from 1-100' # Default response that will only send if input percentage is not 1-100.
        if not valid_response:
            response = f'**Error:** Invalid Damage Type {chr(10)}Supported types: ```{chr(10)}{chr(10).join(csvreader.fieldnames[1:])}```' #using chr(10) as newline, because f-string doesn't support \n
        elif percentage in range(1, 101):
            for row in csvreader:
                ### TODO: Re-evaluate this section to make sure that parsing the csv is as efficient as possible

                # if damage_type not in row.keys(): #Confirm that inputed damage_type is supported by the provided .csv. Otherwise sends error message containing valid types
                #     types = " ".join(row)
                #     types = types.split()[1:]
                #     response = f'**Error:** Invalid Damage Type {chr(10)}Supported types: {chr(10)}{chr(10).join(types)}' #using chr(10) as newline, because f-string doesn't support \n
                #     break
                #print(f' line count: {line_count}, percentage: {percentage} ')
                if line_count == percentage: #line_count will equal percentage when 'row' iterator is the correct row in the critical hit table
                    response = row.get(damage_type.lower()) #Replies with the correspoinding damage effect. Uses 'row' as the dictionary identifier and finds the value assigned to key 'damage_type'
                    break
                else: 
                    line_count += 1 # Incrementing line count effectivly moves the search one row down the table
    await ctx.send(response)

###################
###################
@bot.command(name='spell', help='Search spell definitions')
async def spell_lookup(ctx, spell_name: str):
    '''
    Search for a spell and return its description

    Parameters
    ----------
    ctx : 'discord.ext.commands.Context'
        Message context object from Discord

    spell_name : `str`   
        The name of the spell to search for
    '''

    spell = spell_name.lower()

    with open('spells.json', mode='r', encoding='utf8') as jsonfile:
        spells = json.load(jsonfile)

    embed = discord.Embed(title=f"Can't find spell '{spell}'")
    for s in spells:
        if spell == s.lower():
            embed = helpers.dict_to_embed(s, spells[s])
    await ctx.send(embed=embed)


###################
###################
@bot.command(name='roll_dice', help='Roll virtual dice')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    """
    Simulates rolling of dice

    Parameters
    ----------
    ctx : `discord.ext.commands.Context`
        Message context object from Discord

    number_of_dice : `int`
        The number of dice to be rolled

    number_of_sides : `int`
        How many sides each rolled die should have
    """    
    #Chooses a random int between 1 and the given number of sides
    #Repeats as many times as number_of_dice
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

###################
###################
@bot.command(name='set_activity', help='Set the bot\'s activity')
async def set_act(ctx, activity_type: str, activity_name: str):
    """
    Set the bot's discord activity status

    Parameters
    ----------
    ctx : `discord.ext.commands.Context`
        Message context object from Discord

    activity_type : `str`
        Type of activity to be displayed (e.g. "Playing", "Listening", "Watching")

    activity_name : `str`
        Description of activity to be displayed (e.g. "Playing [activity_name]")
    """    

    if activity_type.lower() == 'playing':
        await bot.change_presence(activity=discord.Game(name=activity_name)) #sets activity to 'Playing activity_name'
    elif activity_type.lower() == 'listening':
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=activity_name)) #sets activity to "Listening to activity_name"
    elif activity_type.lower() == 'watching':
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name= activity_name)) #sets activity to "Watching activity_name"
    else:
        await ctx.send("Activity not supported. Supported Activities: Playing, Listening, Watching") #Sends a list of supported activities if one isn't given

###################
###################
@bot.command(name='meme', help='Dank Me Me')
async def send_meme(ctx):
    """
    Sends a meme to the chat

    Parameters
    ----------
    ctx : `discord.ext.commands.Context`
        Message context object from Discord
    """

    random_meme = random.choice(os.listdir("Memes")) #choose a random file from the "Memes" folder
    while random_meme == ".DS_Store": #If .DS_Store is selected at random, continue choosing until the selected file is NOT .DS_Store
        random_meme = random.choice(os.listdir("Memes"))
    await ctx.send(file=discord.File(f"Memes/{random_meme}"))

###################
###################
@bot.command(name='ping', help="Ping Volobot")
async def ping_response(ctx):
    """
    Responds to a ping request with the estimated ping of the sender

    Parameters
    ----------
    ctx : `discord.ext.commands.Context`
        Message context object from Discord
    """
    embed = discord.Embed(title="Pong!")
    m = await ctx.send(embed=embed)
    ping = (m.created_at-ctx.message.created_at).total_seconds() * 100 #Calculate the time difference between ping request and pong response
    embed.add_field(name=':ping_pong:', value=f'{int(ping)} ms') #Add calculated ping to the embed
    await m.edit(embed=embed) #edit response to include calculated ping (ms)

###################
###################
@bot.command(name='inventory', help="Check the party's inventory")
async def check_inventory(ctx, item: str=None):
    '''
    Displays the contents of inventory.json

    Parameters
    ----------
    ctx : `discord.ext.commands.Context`
        Message context object from Discord

    item : `str`, optional
        The name of the inventory item to list. If ommitted, entire inventory will be listed.
    '''
    with open('inventory.json', mode='r', encoding='utf8') as jsonfile:
        inventory = json.load(jsonfile)

    if(item == None):
        embed = helpers.dict_to_embed("Inventory", inventory)
    else:
        embed = helpers.dict_to_embed(item, inventory[item])

    await ctx.send(embed=embed)

###################
###################
@bot.command(name="store", help="store items in the party's inventory")
async def store_inventory(ctx, item: str, desc: str=None, quant: int=1):
    '''
    Store items in inventory.json

    Parameters
    ----------
    ctx : `discord.ext.commands.Context`
        Message context object from Discord

    item : `str`
        The name of the item to store

    desc : `str`, optional
        A description of the stored item, by default None

    quant : `int`, optional
        The quantity of the item to store, by default 1
    '''
    with open('inventory.json', mode='r', encoding='utf8') as jsonfile:
        inventory = json.load(jsonfile)
    
    if item not in inventory.keys():
        inventory[item] = {"description": desc, "quantity": quant}
    else:
        inventory[item]["quantity"] += quant
        if desc != None:
            inventory[item]["description"] = desc
    
    with open('inventory.json', mode='w') as jsonfile:
        jsonfile.write(json.dumps(inventory, indent=4))

    response = f"Added {quant} {item} to your inventory."

    await ctx.send(response)

###################
###################
@bot.command(name="remove", help="remove items from the party's inventory")
async def remove_inventory(ctx, item: str, quant: int=None):
    '''
    Remove items from inventory.json

    Parameters
    ----------
    ctx : `discord.ext.commands.Context`
        Message context object from Discord

    item : `str`
        The name of the item to remove

    quant : `int`, optional
        The quantity of items to remove, by default all
    '''
    with open('inventory.json', mode='r', encoding='utf8') as jsonfile:
        inventory = json.load(jsonfile)
    
    if quant == None or quant >= inventory[item]["quantity"]:
        del inventory[item]
    else:
        inventory[item]["quantity"] -= quant
    
    with open('inventory.json', mode='w') as jsonfile:
        jsonfile.write(json.dumps(inventory, indent=4))

    response = f"Removed {'all' if quant == None else quant} {item} from your inventory."

    await ctx.send(response)

###############
### RUN BOT ###
###############

bot.run(TOKEN)
