#!/usr/bin/env python

import sys
from discord.ext import commands

# def is_mod():
#     def predicate(ctx):
#         mods = ["Moderator", "Admin", "Junior Mod"]
#         roles = [role.name for role in ctx.message.author.roles]
#         return any(role in mods for role in roles)

#     return commands.check(predicate)

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
            self.bot.load_extension(cog)
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
            self.bot.unload_extension(cog)
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
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            print(f"**`ERROR:`** {type(e).__name__} - {e}", file=sys.stdout)
        else:
            await ctx.send(f"{cog.split('cogs.')[-1]} has been reloaded")

    @commands.command(name="logout", hidden=True, aliases=["goaway"])
    @commands.is_owner()
    async def logout(self, ctx):
        await ctx.bot.logout()

    # @commands.command(name="test", hidden=True)
    # @is_mod()
    # async def logout(self, ctx):
    #     string = [role.name for role in ctx.message.author.roles]
    #     await ctx.send(string)

def setup(bot):
    bot.add_cog(OwnerCog(bot))
