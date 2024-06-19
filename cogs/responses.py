#!/usr/bin/env python
import os
import json

from discord.ext import commands
from .utils import is_mod, user_check

FILE = "statements.json"


class ResponseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="patch", 
        aliases=["patchgulls",],
        help=("Usage: !patch"),
    )
    async def patch(self, ctx):
        patchgulls = "https://cdn.discordapp.com/attachments/174021609475014656/446695427597664265/Patchgulls.png"
        await ctx.send(patchgulls)
        return

    @commands.command(
        name="praise", 
        help=("Usage: !praise"),
    )
    async def patch(self, ctx):
        msg = ":bug:"
        await ctx.send(msg)
        return

    @commands.command(name="dm_commands", help=("Usage: !dm_commands"))
    async def dm_commands(self, ctx):
        with open("statements.json", "r") as reader:
            statements = json.load(reader)
        keys = list(statements.keys())
        commands = "\n".join(keys)
        commands = "**!whatis commands:**\n" + commands

        commands_desc = '**Bot commands:**\n'
        for cog in self.bot.cogs:
            for command in self.bot.get_cog(cog).get_commands():
                # if cog not in a cog
                # listing command if cog name is None and command isn't hidden
                if not command.hidden:
                    commands_desc += f'{command.name}\n'
        output = [commands_desc, commands]
        for description in output:
            await ctx.message.author.send(description)


    @commands.command(name="whatis_commands", help=("Usage: !whatis_commands"))
    async def whatis_commands(self, ctx):
        with open("statements.json", "r") as reader:
            statements = json.load(reader)
        keys = list(statements.keys())
        command = ", ".join(keys)
        await ctx.channel.send(command)

    @commands.command(name="whatis", help=("Usage: !whatis statement"))
    async def whatis(self, ctx, *args):
        statement = " ".join(args)
        statement = statement.lower()
        st_file = open("statements.json", "r")
        statements = json.load(st_file)
        if statement in statements:
            await ctx.channel.send(statements[statement])
        else:
            await ctx.channel.send("I don't know ask Scarlatch.")

    @commands.command(
        name="define_whatis",
        help=(
            "Usage: !define_whatis statement.\nMod only command to add new statements."
        ),
    )
    @commands.check_any(commands.is_owner(), is_mod())
    async def define_whatis(self, ctx, *args):
        """This Command sets the whatis command responses"""
        statement = " ".join(args)
        title = statement.split("-")[0].strip().lower()
        definition = statement.split("-")[1].strip()
        statements = []
        # Add empty file intialisation here
        with open("statements.json", "r") as st_file:
            statements = json.load(st_file)
            statements[title] = definition
        with open("statements.json", "w") as st_file:
            json.dump(statements, st_file, indent=4)


async def setup(bot):
    await bot.add_cog(ResponseCog(bot))


def main():
    return


if __name__ == "__main__":
    main()
