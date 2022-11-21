#!/usr/bin/env python

import discord
import pandas as pd
import numpy as np

from discord.ext import commands
from datetime import datetime


DECKLISTS = "The_Long_Path_5k_Throne_Open_-_Decklists.xlsx"


class DecklistReader():
    """docstring for DecklisReader""" 
    def __init__(self, fname):
        self.sheet_name = fname
        self.df = pd.read_excel(fname, sheet_name=None)
        self.players = list(self.df.keys())

    def player_check(self, query):
        return [key for key in self.players if query.lower() == key.lower()]

    def read_decklist(self, player):
        player_check = self.player_check(player)
        if not player_check:
            return "Player not found"
        out_list = self.df[player_check[0]]["Unnamed: 1"].values[2:]
        out_str = "\n".join(out_list)
        return out_str
        

class DecklistCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.decklist = DecklistReader(DECKLISTS)

    @commands.command(
        name="ecq", help=("Usage: !ecq playername"),
    )
    async def ecq_decklist(self, ctx, *name):
        name = " ".join(name).lower()
        response = self.decklist.read_decklist(name)
        await ctx.send(response)

async def setup(bot):
    await bot.add_cog(DecklistCog(bot))


def main():
    return


if __name__ == '__main__':
    main()
