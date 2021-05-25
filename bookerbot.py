# bookerbot.py
#!/usr/bin/env python


import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from cogs.constants import CHANNELS, PIC_DIR
from cogs.utils import filter_input, in_channel

def main():
    load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")

    bot = commands.Bot(command_prefix="!", case_insensitive=True)

    extensions = [
        "cogs.owner",
        "cogs.setup",
        "cogs.send_pics",
        "cogs.query",
        "cogs.qwant",
        "cogs.birthday",
        "cogs.gfycat",
        "cogs.user_cmd",
        "cogs.responses"
    ]

    for ext in extensions:
        bot.load_extension(ext)

    @bot.event
    async def on_ready():
        print(f"{bot.user} has connected to Discord!")

    @in_channel(*CHANNELS)
    @commands.is_owner()
    @bot.command(
        name="hoppi", help=("Usage: ..."), hidden=True,
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def make_hop_pyramid(ctx, num_pics=1):
        num_pics = filter_input(num_pics, 1, 5)
        emote = "<a:ppHop:475472772072472586>"
        await ctx.send(make_pyramid(emote, num_pics))

    bot.run(TOKEN)


if __name__ == "__main__":
    main()
