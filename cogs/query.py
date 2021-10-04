#!/usr/bin/env python

import os
import random

import discord
from discord.ext import commands
from pathlib import Path

from .constants import CHANNELS, PIC_DIR
from .utils import filter_input, in_channel



def group_name_from_path(path):
    dir_tail = Path(PIC_DIR).name
    current_dir = Path(path)
    idol = current_dir.name
    if current_dir.parts[-2] != dir_tail:
        idol = " ".join(current_dir.parts[-2:])
    return idol


class QueryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.blocked_idols = ["soojin", "olivia"]
        self.blocked_users = []

    @in_channel(*CHANNELS)
    @commands.command(
        name="query",
        help=(
            "Usage: !query (idolgroup)-idolname. Group is an optional input"
        ),
    )
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def query_pics(self, ctx, idol, num_pics=1):
        if idol in self.blocked_idols:
            await getattr(self, f"block_{idol}")(ctx)
            return
        if ctx.author.name.lower() in self.blocked_users:
            await getattr(self, f"block_{ctx.author.name.lower()}")(ctx)
            return
        if "everglow" in idol:
            idol = "yena"

        num_pics = filter_input(num_pics, 1, 5)
        retry_flag = False

        work_dirs = self.bot.get_cog("SetupCog").work_dirs
        if work_dirs is not None:
            VALID_FOLDERS = work_dirs.idol_paths
            ALIAS_FOLDERS = work_dirs.aliases
        else:
            await ctx.send("Directory setup failed.")
            return

        send_pics = self.bot.get_cog("SendPicsCog")
        if send_pics is None:
            await ctx.send("Send pic commands setup failed")
            return

        if idol in ALIAS_FOLDERS.keys():
            idol = ALIAS_FOLDERS[idol]

        if "g-idle" in idol.lower():
            retry_flag = True
            idol_group = "g-idle"
            idol_name = idol.lower().split("g-idle-")[-1]
            idol = os.path.join(idol_group, idol_name)

        elif "-" in idol:
            retry_flag = True
            idol_group, idol_name = idol.lower().split("-")
            if idol_group in ALIAS_FOLDERS.keys():
                idol_group = ALIAS_FOLDERS[idol_group]
            idol = os.path.join(idol_group, idol_name)

        output = []
        for dirs in VALID_FOLDERS:
            if idol.lower() in dirs.lower():
                output.append(dirs)
        if len(output) == 0:
            if retry_flag:
                idol2 = f"{idol_name}-{idol_group}"
                await self.query_pics(ctx, idol2, num_pics)
                return
            await ctx.send(f"{idol} not found.")
            return
        if len(output) > 1:
            names = []
            for dirs in output:
                folder_name = group_name_from_path(dirs)
                names.append(folder_name)
            names = ", ".join(names)
            await ctx.send(
                f"Multiple idols found: **{names}**."
                "\nReply with the group name:"
            )
            message_response = await self.bot.wait_for(
                "message", check=lambda m: m.author == ctx.author
            )
            reply = message_response.content.replace(" ", "")

            for dirs in output:
                folder_name = group_name_from_path(dirs)
                if reply in folder_name.replace(" ", ""):
                    new_query = folder_name.split(" ")
                    idol = new_query[-1]
                    reply = "".join(new_query[:-1])
                    break

            
            await self.query_pics(ctx, f"{reply}-{idol}", num_pics)
            return

        await send_pics.async_send_pics(ctx, num_pics, output[0])

    @in_channel(*CHANNELS)
    @commands.command(
        name="best_girl",
        help=(
            "Usage: !best_girl int to post int pics of a random idol."
            "\nNumber of pics is limited to between 1 and 5."
        ),
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def random_pics(self, ctx, num_pics=1):
        work_dirs = self.bot.get_cog("SetupCog").work_dirs
        if work_dirs is not None:
            VALID_FOLDERS = work_dirs.idol_paths
        else:
            await ctx.send("Directory setup failed.")
            return

        send_pics = self.bot.get_cog("SendPicsCog")
        if send_pics is None:
            await ctx.send("Send pic commands setup failed")
            return

        print("Finding pics")
        num_pics = filter_input(num_pics, 1, 5)
        directory = random.choice(VALID_FOLDERS)
        await send_pics.async_send_pics(ctx, num_pics, directory)

    async def block_soojin(self, ctx):
        pic = os.path.join(
            "C:/", "Users", "will", "Pictures", "no_bullies_allowed.gif"
        )
        file = discord.File(pic)
        await ctx.send(file=file)

    async def block_olivia(self, ctx):
        pic = os.path.join("C:/", "Users", "will", "Pictures", "bolivia.jpg")
        file = discord.File(pic)
        responses = ["Who?", file]
        response = random.choice(responses)
        if isinstance(response, str):
            await ctx.send(response)
        else:
            await ctx.send(file=response)



def setup(bot):
    bot.add_cog(QueryCog(bot))


def main():
    return


if __name__ == "__main__":
    main()
