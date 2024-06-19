#!/usr/bin/env python

import discord
import pandas as pd
import numpy as np

from discord.ext import commands
from datetime import datetime
from .utils import user_check


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

    def read_worlds(self, player):
        player_check = self.player_check(player)
        if not player_check:
            return "Player not found", None

        local_df = self.df[player_check[0]].dropna()
        exp_idx = np.where(local_df.values[:] == 'FORMAT:Expedition')
        exp_idx = exp_idx[0][0]

        throne_list = np.squeeze(local_df.values[:exp_idx]).tolist()
        exp_list = np.squeeze(local_df.values[exp_idx:]).tolist()

        throne_str = "\n".join(throne_list)
        exp_str = "\n".join(exp_list)

        return throne_str, exp_str




class DecklistCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.decklist = DecklistReader(DECKLISTS)
        self.worlds =  DecklistReader("2022_wc_decklists.xlsx")

    @commands.command(
        name="ecq", help=("Usage: !ecq playername"), hidden=True
    )
    @commands.is_owner()
    async def ecq_decklist(self, ctx, *name):
        name = " ".join(name).lower()
        response = self.decklist.read_decklist(name)
        await ctx.send(response)

    @commands.command(
        name="worlds", help=("Usage: !worlds playername")
    )
    @commands.check(user_check())
    async def worlds_decklist(self, ctx, *name):
        name = " ".join(name).lower()
        throne, exp = self.worlds.read_worlds(name)
        await ctx.send(throne)
        if exp is not None:
            await ctx.send(exp)



async def setup(bot):
    await bot.add_cog(DecklistCog(bot))


def main():
    return


if __name__ == '__main__':
    main()
