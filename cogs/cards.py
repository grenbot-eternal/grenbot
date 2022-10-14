import requests
import os
import random
import json
import discord

from pathlib import Path
from urllib.parse import quote
from discord.ext import commands

from .utils import is_mod

HEADERS = [
    {
        "User-Agent": r"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)"
        r"AppleWebKit/537.36 (KHTML, like Gecko)"
        r"Chrome/50.0.2661.102 Safari/537.36"
    }
]


class EWCDownloader:
    """docstring for EWCDownloader"""

    def __init__(self, outdir=None):
        self.json_url = (
            "https://eternalwarcry.com/content/cards/eternal-cards.json"
        )
        self.outdir = outdir

    def request_url(self):
        """Parse EWC for latest card list. Returns json object."""
        headers = random.choice(HEADERS)
        result = requests.get(self.json_url, headers=headers)
        if result.status_code != 200:
            raise ConnectionError(
                f"could not download {self.url}\nerror code: {result.status_code}"
            )
        return result.json()

    def json_to_disk(self):
        outfile_name = "eternal-cards.json"
        if self.outdir is not None:
            outfile_name = os.path.join(self.outdir, outfile_name)
        json_stream = self.request_url()
        with open(outfile_name, "w", encoding="utf-8") as writer:
            json.dump(json_stream, writer, indent=4)


class EternalJsonParser:
    """Parse eternal-cards.json and return key information."""

    def __init__(self, fname, root_dir):
        with open(fname, "r") as reader:
            self.data = json.load(reader)

        if Path("temp-cards.json").is_file():
            with open("temp-cards.json", "r") as reader:
                self.data += json.load(reader)

        self.set_numbers = self.get_unique_set_numbers()
        self.root_dir = root_dir

    def get_unique_set_numbers(self):
        set_numbers = set()
        for item in self.data:
            set_numbers.add(item["SetNumber"])
        return set_numbers

    def get_card_by_name(self, name, ignore_comma=False):
        if not ignore_comma:
            return [
                item
                for item in self.data
                if name.lower() in item["Name"].lower()
            ]
        else:
            return [
                item
                for item in self.data
                if name.lower() in item["Name"].lower().replace(",", "").replace("'", "")
            ]

    def get_card_by_set(self, set_num):
        return [item for item in self.data if set_num == item["SetNumber"]]

    def add_new_set(self):
        """Usage: mod level instead of admin."""
        pic_dir = Path(self.root_dir)
        existing_dirs = [x.name for x in pic_dir.iterdir() if x.is_dir()]
        missing_set_numbers = [
            set_num
            for set_num in self.set_numbers
            if f"Set{set_num}" not in existing_dirs
        ]
        # early exit if no missing sets
        if not missing_set_numbers:
            return "No missing sets found."
        successfull_sets = list(map(str, missing_set_numbers))
        successfull_sets = " ".join(successfull_sets)

        for set_num in missing_set_numbers:
            print(f"Fetching images for set {set_num}")
            self.refresh_set_images(set_num)
        return f"Cards have been added for sets {successfull_sets}."

    def refresh_set_images(self, set_num):
        """Usage: mod level instead of admin."""

        set_num = int(set_num)

        if set_num not in self.set_numbers:
            return f"{set_num} is not a valid set id."

        outdir = os.path.join(self.root_dir, f"Set{set_num}")

        os.makedirs(outdir, exist_ok=True)

        for card in self.get_card_by_set(set_num):
            image = EWCImage(card, self.root_dir)
            image.download_image()
        return f"Images for {set_num} have been redownloaded."


class EWCImage:
    """Container for various name representations of EWC image file"""

    def __init__(self, item, outdir=None):
        self.item = item
        self.imageurl = self.item["ImageUrl"]
        self.setnum = self.item["SetNumber"]
        self.filename = os.path.basename(self.imageurl[:-4]).replace("_", " ")
        self.filepath = f"{self.filename}.png"
        if outdir is not None:
            self.filepath = os.path.join(
                outdir, f"Set{self.setnum}", f"{self.filename}.png"
            )

    def __str__(self):
        return f"Card Image {self.imageurl} - {self.filename} - {self.setnum}"

    def download_image(self):
        headers = random.choice(HEADERS)
        result = requests.get(self.imageurl, headers=headers)

        if result.status_code != 200:
            raise ConnectionError(
                f"could not download {self.imageurl}\nerror code: {result.status_code}"
            )

        print("Downloading to {}".format(self.filepath))

        with open(self.filepath, "wb") as writer:
            writer.write(result.content)

        return f"{self.filename} successfully downloaded."


class CardCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_cards(self, ctx, result):
        image = EWCImage(result, self.bot.image_dir)
        try:
            pic = discord.File(image.filepath)
        except FileNotFoundError:
            await ctx.send(f"Image not found. Redownloading {image.filename}")
            image.download_image()
            pic = discord.File(image.filepath)
        await ctx.send(file=pic)
        return

    @commands.command(
        name="card", help=("Usage: !card cardname"),
    )
    async def cardlookup(self, ctx, *name):
        name = " ".join(name).lower()
        try:
            reader = EternalJsonParser(
                "eternal-cards.json", self.bot.image_dir
            )
            results = reader.get_card_by_name(name)
            if not results:
                results = reader.get_card_by_name(name, ignore_comma=True)
        except Exception as e:
            pass

        if len(results) < 1:
            await ctx.send(f"I don't have any cards matching {name}")
            return

        elif len(results) > 1:
            for result in results:
                namecheck = EWCImage(result, self.bot.image_dir)
                if len(namecheck.filename) == len(name):
                    await self.send_cards(ctx, result)
                    return
            result_names = [
                EWCImage(result, self.bot.image_dir).filename
                for result in results
            ]
            expanded = '"' + '", "'.join(result_names) + '"'

            await ctx.send(
                f"{name} is too general please be more specific:\n{expanded}"
            )
        else:
            await self.send_cards(ctx, results[0])
            return

    @commands.command(
        name="update_card", help=("Usage: !update_card cardname"),
    )
    async def cardUpdate(self, ctx, *name):
        name = " ".join(name).lower()

        reader = EternalJsonParser("eternal-cards.json", self.bot.image_dir)
        results = reader.get_card_by_name(name)
        if len(results) < 1:
            await ctx.send(f"I didn't have any cards matching {name}")
            return
        elif len(results) > 1:
            for result in results:
                result = EWCImage(result, self.bot.image_dir)
                if len(result.filename) == len(name):
                    query_str = result.download_image()
                    await ctx.send(query_str)
                    return
                else:
                    continue
            result_names = [EWCImage(result).filename for result in results]
            expanded = '"' + '", "'.join(result_names) + '"'
            await ctx.send(
                f"{name} is too general please be more specific {expanded}"
            )
            return
        else:
            result = EWCImage(results[0], self.bot.image_dir)
            query_str = result.download_image()
            await ctx.send(query_str)
            return

    @commands.command(
        name="update_set", help=("Usage: !update_set setnumber"),
    )
    @commands.check_any(commands.is_owner(), is_mod())
    async def setUpdate(self, ctx, num):
        try:
            reader = EternalJsonParser(
                "eternal-cards.json", self.bot.image_dir
            )
        except:
            pass
        try:
            result = reader.refresh_set_images(num)
        except Exception as e:
            return
        await ctx.send(result)
        return

    @commands.command(
        name="add_missing_sets", help=("Usage: !add_missing_sets"),
    )
    @commands.check_any(commands.is_owner(), is_mod())
    async def ScrapeMissingSets(self, ctx, renew_json=False):
        if renew_json:
            query_str = renewJSON()
            if "failed" in query_str:
                return query_str

        reader = EternalJsonParser("eternal-cards.json", VAR)
        result = reader.add_new_set()

        await ctx.send(result)
        return

    @commands.command(
        name="renew_json", help=("Usage: !renew_json"),
    )
    @commands.check_any(commands.is_owner(), is_mod())
    async def renewJSON(self, ctx):
        eternal_cards = EWCDownloader()
        eternal_cards.json_to_disk()
        if not Path("eternal-cards.json").is_file():
            await ctx.send(
                "Updating eternal-cards.json failed. Some panic required."
            )
            return
        await ctx.send("eternal-cards.json successfully updated.")
        return



async def setup(bot):
    await bot.add_cog(CardCog(bot))


if __name__ == "__main__":
    main()
