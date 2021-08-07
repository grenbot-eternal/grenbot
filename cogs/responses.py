#!/usr/bin/env python
import os

from discord.ext import commands
from .constants import CHANNELS, PIC_DIR
from .utils import filter_input, in_channel

RESPONSES = {
    "balance": (
        "As always, the community would like to stress that the removal is too good,"
        " the removal is too bad, Tavrod is busted,"
        " DWD needs to print more powerful cards,"
        " Fire doesn't have what it takes, aggro is too strong,"
        " the expensive cards aren't powerful enough,"
        " the big threats are too powerful,"
        " the design pushes midrange as the only viable strategy,"
        " ladder is very healthy and has a lot of variety,"
        " master rank doesn't mean anything,"
        " getting a high rank with a deck makes it good,"
        " there should be more decks that aren't just unit smash,"
        " Chalice is miserable, Time is overpowered, Justice is the most played faction,"
        " your opponent drawing perfectly is absolutely the worst,"
        " and we should drive a spike through variance."
    ),
    "gren": "<:grenWhy:806468021119746108>",
    "alpha": "https://clips.twitch.tv/RudeShyHamWutFace",
    "ilyavsdeathstrike": "https://www.youtube.com/watch?v=w8gASKyO500",
    "modrule": "<a:HarshRule:460979572423262210> THIS ENDS NOW <a:HarshRule:460979572423262210>",
    "beginner_decks": "https://eternalwarcry.com/decks?dn=ultra%20budget&c=AhornDelfin",
    "steve holt": "https://cdn.discordapp.com/attachments/638417442808528916/678671960699437076/eternal_grodovs_stranger.png",
    "nako": "https://streamable.com/5o0t0e",
    "pepsi3": "https://streamable.com/7pv7z1",
    "yoo": "https://streamable.com/uewm9",
    "bunny": "https://streamable.com/tkrbz",
    "hanbin": "https://streamable.com/j9i3gg",
    "spicy": "https://streamable.com/2d5b35",
    "dimples": "https://streamable.com/zc53qa"
}


RESPONSE_FILTER = ["nako", "hanbin", "pepsi3", "yoo", "bunny", "spicy", "dimples"]

RESPONSE_FILTERED = {
    key: value for key, value in RESPONSES.items() if key in RESPONSE_FILTER
}

class ResponseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.make_commands()

    def make_bot_command(self, key, response):
        @in_channel(*CHANNELS)
        @commands.cooldown(1, 10, commands.BucketType.user)
        async def bot_send_string(self, ctx):
            await ctx.send(response)
        com = commands.command(
                name=key,
                )(bot_send_string)
        return com

    def make_commands(self):
        command_list = []
        for key, item in RESPONSE_FILTERED.items():
            com = self.make_bot_command(key, item)
            command_list.append(com) 
        self.__cog_commands__ = tuple(command_list)           

def setup(bot):
    bot.add_cog(ResponseCog(bot))

def main():
    return


if __name__ == "__main__":
    main()
