import discord

########################
### HELPER FUNCTIONS ###
########################
def dict_to_embed(title, d):
    '''
    Convert a Python Dictionary to a Discord Embed

    Parameters
    ----------
    title : `str`
        the title of the Discord Embed

    d : `dict`
        Dictionary object

    Returns
    -------
    `discord.Embed`
        Discord Embed object
    '''
    
    embed = discord.Embed(title=title)
    for o in d:
        if o == "description":
            embed.description=d[o]
        else:
            if isinstance(d[o], dict):
                val = ""
                for key in d[o]:
                    val += f"{key}: {d[o][key]}\n\n"
            else:
                val = d[o]
            embed.add_field(name=f"{o}", value=f'{val}', inline=False)
        
    return embed