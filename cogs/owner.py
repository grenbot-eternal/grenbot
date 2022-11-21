#!/usr/bin/env python

import sys
from discord.ext import commands


class OwnerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Hidden means it won't show up on the default help.
    @commands.command(name="load", hidden=True)
    @commands.is_owner()
    async def load(self, ctx, cog: str):
        if "cogs." not in cog:
            cog = f"cogs.{cog}"
        try:
            await self.bot.load_extension(cog)
        except Exception as e:
            print(f"**`ERROR:`** {type(e).__name__} - {e}", file=sys.stdout)
        else:
            await ctx.send(f"{cog.split('cogs.')[-1]} has been loaded")

    @commands.command(name="unload", hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, cog: str):
        if "cogs." not in cog:
            cog = f"cogs.{cog}"
        try:
            await self.bot.unload_extension(cog)
        except Exception as e:
            print(f"**`ERROR:`** {type(e).__name__} - {e}", file=sys.stdout)
        else:
            await ctx.send(f"{cog.split('cogs.')[-1]} has been unloaded")

    @commands.command(name="reload", hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, cog: str):
        if not cog:
            await ctx.send("Reload requires cog argument.")
            return
        if "cogs." not in cog:
            cog = f"cogs.{cog}"
        try:
            await self.bot.unload_extension(cog)
            await self.bot.load_extension(cog)
        except Exception as e:
            print(f"**`ERROR:`** {type(e).__name__} - {e}", file=sys.stdout)
        else:
            await ctx.send(f"{cog.split('cogs.')[-1]} has been reloaded")


    @commands.command(name="speak", hidden=True)
    @commands.is_owner()
    async def speak(self, ctx, *kwargs: str):
        off_topic = 176876742118473729
        general = 174021609475014656
        channel = self.bot.get_channel(general)
        phrase = " ".join(kwargs)
        await channel.send(phrase)

async def setup(bot):
    await bot.add_cog(OwnerCog(bot))
