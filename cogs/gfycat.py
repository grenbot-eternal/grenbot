#!/usr/bin/env python

import requests
import random
import json

from discord.ext import commands

from .utils import in_channel, filter_input
from .constants import CHANNELS

HEADERS = [
    {
        "User-Agent": r"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)"
        r"AppleWebKit/537.36 (KHTML, like Gecko)"
        r"Chrome/50.0.2661.102 Safari/537.36"
    }
]
NUM_MAX = 5
NUM_MIN = 1

EXCEPTIONS = {"choerry": "최리"}

def main():
    # Tests
    return


class GfycatSearch:
    """docstring for GfycatSearch"""

    def __init__(self, query, num_pics):
        self.num_pics = filter_input(num_pics, NUM_MIN, NUM_MAX)
        self.url = self.gfy_url(query)
        self.api_response = json.loads(self.request_url())
        if self.api_response["found"] == 0:
            raise UserWarning(
                f"API request failed with no results found."
            )

    def gfy_url(self, query):
        url = (
            f"https://api.gfycat.com/v1/gfycats/search?search_text="
            f"{query}&count=20"
        )
        return url

    def request_url(self):
        headers = random.choice(HEADERS)
        result = requests.get(self.url, headers=headers)
        if result.status_code != 200:
            raise ConnectionError(
                f"could not download {self.url}\nerror code: {result.status_code}"
            )
        return result.content

    def api_to_image(self):
        """Returns a list of image urls from the api json response."""
        output = [
            f"https://gfycat.com/{item['gfyName']}"
            for item in self.api_response['gfycats']
        ]
        try:
            sample = random.sample(output, self.num_pics)
        except ValueError:
            sample = output
        return sample


class GfycatCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @in_channel(*CHANNELS)
    @commands.command(
        name="gfycat", aliases=["gfy",],
        help=("Usage: g!fycat query. Uses gfycat API to return gifs."),
    )
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def gfy_search(self, ctx, *idol, num_pics=1):
        blocked = ["soda", "feets", "feet", "foot", "olivia", "olivi", "eunbig", "pit"]
        try:
            num_pics = int(idol[-1])
            idol = idol[:-1]
        except ValueError:
            pass
            
        if any(x.lower() in blocked for x in idol):
             return
        if ctx.author.name.lower() == "addem":
            if any("fap" in x.lower() for x in idol):
                return

        idol = "+".join(idol)
        for key, item in EXCEPTIONS.items():
            if key in idol:
                idol = idol.replace(key, item)
        api_request = GfycatSearch(idol, num_pics)
        images = api_request.api_to_image()
        async with ctx.typing():
            await ctx.send("\n".join(images))

def setup(bot):
    bot.add_cog(GfycatCog(bot))


if __name__ == "__main__":
    main()
