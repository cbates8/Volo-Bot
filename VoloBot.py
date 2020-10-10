#####################################
#####################################
# VoloBot.py
# Author: Casey Bates
# https://github.com/cbates8/Volo-Bot
#####################################
#####################################
import os
import random
import csv

import discord
from dotenv import load_dotenv

from discord.ext import commands

description = '''A Dungeons and Dragons bot based on Volothamp Geddarm.

Capable of rolling dice, checking critical hit tables, and more!'''

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') #gets DISCORD_TOKEN from token specified in the .env file
GUILD = os.getenv('DISCORD_GUILD') #gets DISCORD_GUILD from guild ID specified in the .env file

#command_prefix= defines the bot's command prefix (string)
#description= will add a description to the !help menu (string)
bot = commands.Bot(command_prefix='!', description=description)

# On ready, bot will print to the console confirming its connection to discord, as well as the guild specified in the .env file
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f'{bot.user.name} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    #set activity status to "Playing Dungeons and Dragons"
    #await bot.change_presence(activity=discord.CustomActivity(name="Reading \'Volo\'s Guide to Monsters\'", emoji=None, type=discord.ActivityType.custom))
    await bot.change_presence(activity=discord.Game(name="Dungeons and Dragons"))

#When seeing a message containing 'volo', bot will reply with a random quote from the list stored in volo_quotes
@bot.event
async def on_message(message):
    #checks if the bot was the one to send the message. If so, breaks out of function to avoid a continuous reply to itself
    if message.author == bot.user:
        return

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

#Search the provided .csv of the crititcal hit table using the user's inputed percentage and damage type. Reply with the resulting effect
@bot.command(name='crit', help='Search the critical hit table')
async def crit_roll(ctx, percentage: int, damage_type: str):
    # Default response that will only send if input percentage is not 1-100.
    response = 'Error: Invalid Percentage Roll'

    #Abreviation support for damge types (spelling bludgeoning is hard!)
    damage_type = damage_type.lower()
    switcher = { #makeshift switch-case statement using dictionary mappings
        'sl': 'slashing',
        'bl': 'bludgeoning',
        'pi': 'piercing',
        'fi': 'fire',
        'co': 'cold',
        'li': 'lightning',
        'fo': 'force',
        'ne': 'necrotic',
        'ra': 'radiant',
        'ac': 'acid',
        'ps': 'psychic',
        'th': 'thunder'
    } 
    damage_type = switcher.get(damage_type, "Invalid Damage Type")

    #Opens 'Critical Hit Table.csv' and treats it as a dictionary. First row treated as keys, with following rows each being its own set of values for those keys
    with open('Critical Hit Table.csv', mode='r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        line_count = 1
        for row in csvreader:
            if damage_type not in row.keys(): #Confirm that inputed damage_type is supported by the provided .csv. Otherwise sends error message containing valid types
                response = f'**Error:** Invalid Damage Type. \nSupported types: {"\n".join(row[1:])}'
                break
            #print(f' line count: {line_count}, percentage: {percentage} ')
            if line_count == percentage: #line_count will equal percentage when 'row' iterator is the correct row in the critical hit table
                response = row.get(damage_type.lower()) #Replies with the correspoinding effect. Uses 'row' as the dictionary identifier and finds the value assigned to key 'damage_type'
                break
            else: # Incrementing line count effectivly moves the search one row down the table
                line_count += 1
    await ctx.send(response)

# Simulates rolliung of dice
@bot.command(name='roll_dice', help='Roll virtual dice')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    #Chooses a random int between 1 and the given number of sides
    #Repeats as many times as number_of_dice
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

#Set the bot's discord activity status
@bot.command(name='set_activity', help='Set the bot\'s activity')
async def set_act(ctx, activity_type: str, activity_name: str):
    if activity_type.lower() == 'playing':
        await bot.change_presence(activity=discord.Game(name=activity_name)) #sets activity to 'Playing activity_name'
    elif activity_type.lower() == 'listening':
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=activity_name)) #sets activity to "Listening to activity_name"
    elif activity_type.lower() == 'watching':
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name= activity_name)) #sets activity to "Watching activity_name"
    else:
        await ctx.send("Activity not supported. Supported Activities: Playing, Listening, Watching") #Sends a list of supported activities if one isn't given

#Sends a meme to the chat
@bot.command(name='meme', help='Dank Me Me')
async def send_meme(ctx):
    random_meme = random.choice(os.listdir("Memes")) #choose a random file from the "Memes" folder
    while random_meme == ".DS_Store": #If .DS_Store is selected at random, continue choosing until the selected file is NOT .DS_Store
        random_meme = random.choice(os.listdir("Memes"))
    await ctx.send(file=discord.File(f"Memes/{random_meme}"))

bot.run(TOKEN)
