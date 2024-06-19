#!/usr/bin/env python

import discord
import pandas as pd
import numpy as np

from discord.ext import commands
from datetime import datetime
from scipy.stats import hypergeom, multivariate_hypergeom

from .utils import user_check


def pmf_at_least_one(distribution, total_draws):
    val = 0.0
    # Calc odds to draw less than 1 of both and inverse
    for i in list(range(1, total_draws + 1)):
        val += dist.pmf(x=[i, 0, total_draws - i])
        val += dist.pmf(x=[0, i, total_draws - i])
    val += dist.pmf(x=[0, 0, total_draws])

    return 1 - val


def prettify_odds(float_val):
    float_val *= 100
    string = f"{float_val:.2f}%"
    return string


class StatsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="multivar",
        help=("Usage: !multivar DRAWS NUM_CARD1 NUM_CARD2 DECKSIZE=75"),
    )
    async def ecq_decklist(
        self,
        ctx,
        draws: int = commands.parameter(description="Sample size drawn from the deck"),
        num_card1: int = commands.parameter(
            description="Number of card type 1 in the deck"
        ),
        num_card2: int = commands.parameter(
            description="Number of card type 2 in the deck"
        ),
        decksize: int = commands.parameter(default=75, description="Total deck size"),
    ):
        for user_arg in [draws, num_card1, num_card2]:
            if user_arg >= decksize:
                await ctx.send(f"Input {user_arg} is larger than the decksize {decksize}")
                return

        if draws < 1:
            await ctx.send(f"Sample size {draws} is invalid")
            return

        num_other = decksize - num_card1 - num_card2
        dist = multivariate_hypergeom(m=[num_card1, num_card2, num_other], n=draws)

        odds = pmf_at_least_one(dist, draws)
        response = prettify_odds(odds)
        response += f" to draw at least one card of both types in {draws} cards"
        await ctx.send(response)

    @commands.command(
        name="draws", help=("Usage: !draws DRAWS GEQ_VALUE NUM_CARD_TOTAL DECKSIZE=75")
    )
    async def worlds_decklist(
        self,
        ctx,
        draws: int = commands.parameter(description="Sample size drawn from the deck"),
        geq_value: int = commands.parameter(
            description="Minimal number of cards in the sample"
        ),
        num_card: int = commands.parameter(
            description="Number of target cards in the deck"
        ),
        decksize: int = commands.parameter(default=75, description="Total deck size"),
    ):
        for user_arg in [draws, geq_value, num_card]:
            if user_arg > decksize:
                await ctx.send(f"Input {user_arg} is larger than the decksize {decksize}")
                return
        if draws < 1:
            await ctx.send(f"Sample size {draws} is invalid")
            return
        if geq_value < 1 or geq_value > draws:
            error_msg = f"Number of successes in sample, {geq_value}, is invalid and "
            if geq_value < 1:
                error_msg += "can't be less than 1"
            else:
                error_msg += f"can't be more than number of draws, {draws}"
            await ctx.send(error_msg)
            return
        rv = hypergeom(decksize, num_card, draws)

        odds = rv.sf(geq_value - 1)
        response = prettify_odds(odds)
        response += f" to draw at least {geq_value} in {draws} cards"
        await ctx.send(response)


async def setup(bot):
    await bot.add_cog(StatsCog(bot))


def main():
    return


if __name__ == "__main__":
    main()
