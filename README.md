# VoloBot - A D&D Discord Bot

A simple Dungeons and Dragons themed Discord Bot. Named for the famed [Volothamp Geddarm](https://forgottenrealms.fandom.com/wiki/Volothamp_Geddarm) of Waterdeep, this bot can roll virtual dice, read an extensive critical hit table, scrape the web for spell descriptions, and much more!

## Commands:

### !roll \<number_of_dice\> \<number_of_sides\>

VoloBot will roll the specified number of dice, each with the specified number of sides.

EX: **'!roll 3 6'** will tell VoloBot to roll 3 6-Sided dice.

![roll example](https://raw.githubusercontent.com/cbates8/Volo-Bot/main/Command%20Examples/roll_example.png)

### !crit \<crit_percentage\> \<dmg_type\>

VoloBot will take a percentage (1-100) and a type of damage (slashing, bludgeoning, piercing, fire, cold, lightning, force, necrotic, radiant, acid, psychic, thunder), and reply with the corresponding effect from the critical hit table.

Note: Percentages and damage types based on 'Critical_Hit_Table.csv'. Using two letter abbreviations (such as 'bl' instead of 'bludgeoning') are also supported.

EX: **'!crit 40 slashing'** will send the corresponding effect of a 40% roll with a damage type of 'slashing'.

![crit example](https://raw.githubusercontent.com/cbates8/Volo-Bot/main/Command%20Examples/crit_example.png)

### !spell \<spell_name\> \<source\>

Search spell descriptions. VoloBot will first check [spells.json](https://github.com/cbates8/Volo-Bot/blob/main/spells.json) for locally stored information to improve response time and support homebrew spells. If a spell is not found locally, VoloBot will search for the spell on [D&D Beyond](https://www.dndbeyond.com/).

EX: **'!spell fireball'** will send the description of spell 'fireball'.

![spell example 1](https://raw.githubusercontent.com/cbates8/Volo-Bot/main/Command%20Examples/spell_example_1.png)

EX: **'!spell fireball web'** will send the description of spell 'fireball' as found on D&D Beyond, skipping local search.

![spell example 2](https://raw.githubusercontent.com/cbates8/Volo-Bot/main/Command%20Examples/spell_example_2.png)

### !store \<item\> \<description\> \<quantity\>

Add items to VoloBot's virtual inventory.

EX: **'!store "health potion" "Restores 2d4 + 2 HP" 2'**

![spell example 2](https://raw.githubusercontent.com/cbates8/Volo-Bot/main/Command%20Examples/store_example.png)

### !bag \<item\>

List items stored in VoloBot's virtual inventory. Specifying an item will give more information about that item.

EX: **'!bag'**

![spell example 2](https://raw.githubusercontent.com/cbates8/Volo-Bot/main/Command%20Examples/bag_example.png)

### !remove \<item\> \<quantity\>

Remove items from VoloBot's virtual inventory.

EX: **'!remove "health potion" 1'**

![spell example 2](https://raw.githubusercontent.com/cbates8/Volo-Bot/main/Command%20Examples/remove_example.png)

### !ping

Check the latency between the sender and VoloBot.

EX: **'!ping'**

![spell example 2](https://raw.githubusercontent.com/cbates8/Volo-Bot/main/Command%20Examples/ping_example.png)

### !set_activity \<activity_type\> \<activity_name\>

Set VoloBot's Discord activity status, where \<activity_type\> is one of 'Playing', 'Listening', or 'Watching'.

EX: **'!set_activity playing D&D'** will set VoloBot's Discord status to _'Playing D&D'_.

![set_activity example 1](https://raw.githubusercontent.com/cbates8/Volo-Bot/main/Command%20Examples/set_activity_example_1.png)
![set_activity example 2](https://raw.githubusercontent.com/cbates8/Volo-Bot/main/Command%20Examples/set_activity_example_2.png)

### !meme

VoloBot will reply with a random meme.

![meme example](https://raw.githubusercontent.com/cbates8/Volo-Bot/main/Command%20Examples/meme_example.png)

## Dependencies (see `requirements.txt`):

### discord.py

`pip3 install discord.py`

### dotenv

`pip3 install python-dotenv`

### beautifulsoup4

`pip3 install beautifulsoup4`

### csv.py

This module is included with Python 3.9. For versions of Python 3 below 3.9, you can download the module [here](https://github.com/python/cpython/blob/3.8/Lib/csv.py).
