#!/usr/bin/env python
import os
import random

from discord.ext import commands
from .constants import CHANNELS, PIC_DIR
from .utils import filter_input, in_channel

USER_COMMANDS = {
    "andy": ["fromis9", "chaeyoung"],
    "mowe": ["twice", "dubu"],
    "mac": ["wekimeki", "elly"],
    "aku": ["twice", "nayeon"],
    "macko": ["clc", "yujin"],
    "pym": ["dreamcatcher", "gahyeon"],
    "accpi": ["wjsn", "lewda"],
    "sheep": ["dreamcatcher", "jiu"],
    "wheel": ["twice", "Jeongyeon"],
    "daisy": ["loona", "Jinsoul"],
    "tsuku": ["dreamcatcher", "yoohyeon"],
    "maddi": ["dreamcatcher", "dami"],
    "smithy": ["oh my girl", "hyojung"],
    "navi": ["itzy", "yeji"],
    "elain": ["oh my girl", "yooa"],
    "moomin": ["loona", "kim_lip"],
    "ginger": ["g-idle", "soyeon"],
    "rave": ["loona", "vivi"],
    "elmerion": ["red velvet", "wendy"],
    "meg": ["oh my girl", "seunghee"],
    "freya": ["loona", "heejin"],
    "addem": ["twice", "sana"],
    "mugi": ["kard", "bm"]
}

TEST_USERS = {"booker": ["dreamcatcher", "Sua"],
              "addem": ["wjsn", "yeonjung"]
}

class CmdCog(commands.Cog):
    """docstring for CmdCog"""
    def __init__(self, bot, cmd_name, cmd_dir):
        self.bot = bot
        self.cmd_name = cmd_name
        self.cmd_dir = cmd_dir

    @in_channel(*CHANNELS)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def send_idol_pics(self, cog, ctx, num_pics=1):
        send_pics = self.bot.get_cog("SendPicsCog")
        if send_pics is None:
            await ctx.send("Send pic commands setup failed")
            return
        item = self.cmd_dir
        num_pics = filter_input(num_pics, 1, 5)
        directory = os.path.join(PIC_DIR, *item)
        print("Finding pics")
        await send_pics.async_send_pics(ctx, num_pics, directory)
            

class UserCmdCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.make_commands()

    def make_commands(self):
        command_list = []
        for key, item in USER_COMMANDS.items():
            com = commands.command(
                name=key,
                help=(
                        f"Usage: !{key} int to post int pics of "
                        f"{item[-1].lower().replace('_', ' ')}."
                        f"\nNumber of pics is limited to between 1 and 5."
                    ),
                )(CmdCog(self.bot, key, item).send_idol_pics)
            command_list.append(com) 
        self.__cog_commands__ = tuple(command_list)           


                

def setup(bot):
    bot.add_cog(UserCmdCog(bot))


def main():
    # To-do: Add json dump?
    return


if __name__ == "__main__":
    main()
