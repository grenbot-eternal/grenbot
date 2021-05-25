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


def main():
    # Tests
    return


class QwantSearch:
    """docstring for QwantSearch"""

    def __init__(self, query, num_pics):
        num_pics = filter_input(num_pics, NUM_MIN, NUM_MAX)
        self.url = self.qwant_url(query, num_pics)
        self.api_response = json.loads(self.request_url())
        if self.api_response["status"] != "success":
            raise UserWarning(
                f"API request failed with error {self.api_response['status']}"
            )

    def qwant_url(self, query, num_pics):
        url = (
            f"https://api.qwant.com/api/search/"
            f"images?uiv=4&q={query}&t={query}&count={num_pics}"
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
            item["media"]
            for item in self.api_response["data"]["result"]["items"]
        ]
        return output


class QwantCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @in_channel(*CHANNELS)
    @commands.command(
        name="search",
        help=("Usage: !search query. Uses qwant API to return images."),
    )
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def qwant_search(self, ctx, *idol, num_pics=1):
        try:
            num_pics = int(idol[-1])
            idol = idol[:-1]
        except ValueError:
            pass
        idol = " ".join(idol)
        api_request = QwantSearch(idol, num_pics)
        images = api_request.api_to_image()
        await ctx.send("\n".join(images))


def setup(bot):
    bot.add_cog(QwantCog(bot))


if __name__ == "__main__":
    main()
