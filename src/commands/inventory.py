"""Inventory Commands"""

from discord.ext.commands import Bot, Cog, Context, command, parameter

from utils.embed import dict_to_embed
from utils.utils import load_json, write_json


class Inventory(Cog):

    def __init__(self: "Inventory", bot: Bot):
        self.bot = bot

    @command(name="bag", help="Check the party's inventory")
    async def check_inventory(
        self: "Inventory",
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

    @command(name="store", help="Store items in the party's inventory")
    async def store_inventory(
        self: "Inventory",
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

    @command(name="remove", help="Remove items from the party's inventory")
    async def remove_inventory(
        self: "Inventory",
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


async def setup(bot: Bot):
    await bot.add_cog(Inventory(bot))
