#!/usr/bin/env python

import os
from pathlib import Path

from discord.ext import commands

from .constants import PIC_DIR

EXCEPTIONS = [
    "dc_site",
    "gfycat",
    "gif",
    "korean_part_1",
    "kpop wallpapers",
    "mac gifs",
    "nca",
    "pic grabber",
    "sohye",
    "streamable",
    "twitter",
]
MEMBER_EXCEPTIONS = ["naver", "Minx", "photobooks"]

def extra_aliases(output_dict):
    output_dict["luda"] = "lewda"
    output_dict["dahyun"] = "dubu"
    output_dict["yorm"] = "yeoreum"
    output_dict["romsae"] = "saerom"
    return output_dict

class BotSetup:
    """docstring for BotSetup"""

    def __init__(self, root_dir):
        self.root = Path(root_dir)
        self.groups = [
            x.name
            for x in self.root.iterdir()
            if x.is_dir() and x.name not in EXCEPTIONS
        ]
        self.aliases = self.generate_aliases()
        self.idol_paths = self.generate_child_folders()

    def generate_child_folders(self):
        output = []
        for group in self.groups:
            path = Path(f"{self.root}/{group}")
            members = [
                str(x)
                for x in path.iterdir()
                if x.is_dir() and x.name not in MEMBER_EXCEPTIONS
            ]
            if not members:
                members = [str(path)]
            output += members
        return output

    def generate_aliases(self):
        output_dict = {}
        for group in self.groups:
            if " " in group:
                alias = group.replace(" ", "")
                output_dict[alias] = group
        extra_aliases(output_dict)
        return output_dict

class SetupCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.work_dirs = BotSetup(PIC_DIR)

def setup(bot):
    bot.add_cog(SetupCog(bot))