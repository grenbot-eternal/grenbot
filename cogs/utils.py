#!/usr/bin/env python

from discord.ext import commands

# Collection of utility functions


def in_channel(*channels):
    def predicate(ctx):
        return ctx.channel.name in channels

    return commands.check(predicate)


def filter_input(num_pics, minimum=1, maximum=5):
    try:
        num_pics = int(num_pics)
    except ValueError:
        num_pics = 1
    return max(min(num_pics, maximum), minimum)
