# grenbot.py
#!/usr/bin/env python

import os

import discord

from discord.ext import commands
from dotenv import load_dotenv

CARD_IMAGES = os.path.join("D:\\", "grenbot", "cards")

class GrenBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(
            command_prefix="!", case_insensitive=True, intents=intents
        )
        self.image_dir = CARD_IMAGES
        os.makedirs(self.image_dir, exist_ok=True)

    async def setup_hook(self):
        extensions = [
            "cogs.cards",
            "cogs.owner",
            "cogs.responses",
            "cogs.ecq",
        ]
        for ext in extensions:
            await self.load_extension(ext)


def main():
    load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")

    bot = GrenBot()

    # @bot.event
    # async def on_message(message):
    #     if message.author.name.lower() != "mail":
    #         if message.content.endswith("?"):
    #             await message.channel.send("Depends on the context.")
    #         await bot.process_commands(message)

    bot.run(TOKEN)


if __name__ == "__main__":
    main()
