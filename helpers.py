import discord

########################
### HELPER FUNCTIONS ###
########################
def generate_spell_embed(sName, jObject):
    embed = discord.Embed(title=sName)
    for o in jObject:
        if o == "description":
            embed.description=jObject[o]
        else:
            embed.add_field(name=f"{o}", value=f'{jObject[o]}', inline=False)
        
    return embed