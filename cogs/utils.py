#!/usr/bin/env python

from discord.ext import commands

# Collection of utility functions


def in_channel(*channels):
    def predicate(ctx):
        try:
            return ctx.channel.name in channels
        except AttributeError:
            return True

    return commands.check(predicate)


def is_mod():
    def predicate(ctx):
        # Workaround for the owner
        mods = ["Moderator", "Admin", "Junior Mod"]
        roles = [role.name for role in ctx.message.author.roles]
        try:
            return any(role in mods for role in roles)
        except AttributeError:
            return True

    return commands.check(predicate)

