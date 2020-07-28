# VoloBot - A D&D Discord Bot

A simple Dungeons and Dragons themed Discord Bot. Named for the famed [Volothamp Geddarm](https://forgottenrealms.fandom.com/wiki/Volothamp_Geddarm) of Waterdeep, this bot can roll virtual dice, read an extensive critical hit table, respond to its own name, and even post memes!

## Commands:

### !roll_dice <number_of_dice> <number_of_sides>
VoloBot will roll the specified number of dice, each with the specified number of sides.

EX: **'!roll_dice 3 6'** will tell VoloBot to roll 3 6-Sided dice.

![roll_dice example](https://github.com/cbates8/Volo-Bot/blob/master/Command%20Examples/roll_dice%20example.png)

### !crit <percentage> <damage_type>
VoloBot will take a percentage (1-100) and a type of damage (slashing, bludgeoning, piercing, fire, cold, lightning, force, necrotic, radiant, acid, psychic, thunder), and reply with the corresponding effect from the critical hit table.

Note: Percentages and damage types based on 'Critical Hit Table.csv'. Using a different table might require different damage types.

EX: **'!crit 40 slashing'** will send the corresponding effect of a 40% roll with a damage type of 'slashing'.

![crit example](https://github.com/cbates8/Volo-Bot/blob/master/Command%20Examples/crit%20example.png)

### !set_activity <activity_type> <activity_name>
Set VoloBot's Discord activity status, where <activity_type> is one of *'Playing'*, *'Listening'*, or *'Watching'*.

EX: **'!set_activity playing D&D'** will set VoloBot's Discord status to *'Playing D&D'*.

![set_activity example 1](https://github.com/cbates8/Volo-Bot/blob/master/Command%20Examples/set_activity%20example%201.png)
![set_activity example 2](https://github.com/cbates8/Volo-Bot/blob/master/Command%20Examples/set_activity%20example%202.png)

### !meme
VoloBot will reply with a random meme from the "Memes" folder.

![meme example](https://github.com/cbates8/Volo-Bot/blob/master/Command%20Examples/meme%20example.png)

## Dependencies:

### discord.py
`pip install discord.py`

### dotenv
`pip install python-dotenv`

### csv.py
This module is supposed to be included with Python 3.x, but for some reason I couldn't get it to work natively.
So, I downloaded it from [here](https://github.com/python/cpython/blob/3.8/Lib/csv.py)
