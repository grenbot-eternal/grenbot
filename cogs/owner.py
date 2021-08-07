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

    async def id_2_user(self, ctx, usr_id: str):
        """Return discord User object from user input"""
        try:
            usr_id = int(usr_id)
            user = await self.bot.fetch_user(usr_id)
        except ValueError:
            # Except block to return user id from name
            user = await ctx.message.guild.query_members(usr_id)

            if len(user) > 1:
                name = [name for usr in user if len(usr.name) == len(usr_id)]
                if len(name) == 1:
                    user = name
                # error handling
                elif len(name) > 1:
                    await ctx.send("Multiple users found. Please be specific.")
                    return None
                else:
                    await ctx.send("No user found.")
                    return None
        return user[0]

    @commands.command(name="test", hidden=True)
    @commands.is_owner()
    async def check_id(self, ctx, *usr_id):
        if not usr_id:
            usr_id = ctx.message.author.id
        else:
            usr_id = " ".join(usr_id)

        user = await self.id_2_user(ctx, usr_id)

        if user is None:
            return


#check message history
#make embed
        string = f"{user.id}"
        await ctx.send(string)

def setup(bot):
    bot.add_cog(OwnerCog(bot))
