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
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!', description=description)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f'{bot.user.name} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    #await bot.change_presence(activity=discord.CustomActivity(name="Reading \'Volo\'s Guide to Monsters\'", emoji=None, type=discord.ActivityType.custom))
    await bot.change_presence(activity=discord.Game(name="Dungeons and Dragons"))

@bot.event
async def on_message(message):
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

    if 'volo' in message.content.lower():
        response = random.choice(volo_quotes)
        await message.channel.send(response)
    await bot.process_commands(message)


@bot.command(name='crit', help='Search the critical hit table')
async def crit_roll(ctx, percentage: int, damage_type: str):
    # Default response that will send if input percentage is not 1-100.
    response = 'Error: Invalid Percentage Roll'

    with open('Critical Hit Table.csv', mode='r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        line_count = 1
        for row in csvreader:
            if damage_type not in row.keys():
                response = f'Error: Invalid Damage Type. Supported types: {", ".join(row)}'
                break
            #print(f' line count: {line_count}, percentage: {percentage} ')
            if line_count == percentage:
                response = row.get(damage_type.lower())
                break
            else:
                line_count += 1
    await ctx.send(response)


@bot.command(name='roll_dice', help='Rolls virtual dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))


@bot.command(name='set_activity', help='Set the bot\'s activity')
async def set_act(ctx, activity_type: str, activity_name: str):
    if activity_type.lower() == 'playing':
        await bot.change_presence(activity=discord.Game(name=activity_name))
    elif activity_type.lower() == 'listening':
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=activity_name))
    elif activity_type.lower() == 'watching':
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name= activity_name))
    else:
        await ctx.send("Activity not supported. Supported Activities: Playing, Listening, Watching")

@bot.command(name='meme', help='Dank May May')
async def send_meme(ctx):
    random_meme = random.choice(os.listdir("Memes"))
    while random_meme == "DS_Store":
        random_meme = random.choice(os.listdir("Memes"))
    await ctx.send(file=discord.File(f"Memes/{random_meme}"))

bot.run(TOKEN)
