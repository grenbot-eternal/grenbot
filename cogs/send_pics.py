#!/usr/bin/env python

import os
import random
import sys

import discord
from discord.ext import commands


class ByteRepresentation:
    """docstring for ByteRepresentation"""

    def __init__(self, file):
        size = os.path.getsize(file)
        self.b = size
        self.kb = size / 1024
        self.mb = size / (1024 ** 2)
        self.gb = size / (1024 ** 3)


class DiscordPic:
    """docstring fos DiscordPic"""

    def __init__(self, num_pics, directory, pics_only=False):
        self.directory = directory
        self.num_pics = num_pics
        self.pics_only = pics_only
        self.pics = self.get_pics()

    def generate_img_list(self):
        file_exceptions = ["ini"]
        if self.pics_only:
            vid_extensions = ["mp4", "gif"]
            file_exceptions += vid_extensions
        files = []
        for dirname, dirnames, filenames in os.walk(self.directory):
            for file in filenames:
                if file.split(".")[-1] not in file_exceptions:
                    files.append(os.path.join(self.directory, file))
            break
        return files

    def get_pics(self):
        print(self.directory)
        pics = self.generate_img_list()
        try:
            pic = random.sample(pics, self.num_pics)
        except ValueError:
            pic = [random.choice(pics)]
        return pic

    def chunk_image_lists(self, chunk_limit=8.0):
        """Chunk list into 8mb subchunks"""
        output = []
        chunk = []
        chunk_size = 0
        for file in self.pics:
            file_size = ByteRepresentation(file).mb
            if file_size >= chunk_limit:
                print(
                    f"{file} has been discarded with size {file_size:.2f}MB."
                )
                continue
            chunk_size += file_size
            if chunk:
                if chunk_size <= chunk_limit:
                    chunk.append(file)
                else:
                    output.append(chunk)
                    chunk = [file]
                    chunk_size = file_size
            else:
                chunk = [file]
        else:
            output.append(chunk)
        return output


class SendPicsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def async_send_pics(self, ctx, num_pics, directory):
        pic_list = DiscordPic(num_pics, directory)
        print("Pics found.")
        files = [discord.File(pic) for pic in pic_list.pics]
        print("Sending pics")
        try:
            async with ctx.typing():
                await ctx.send(files=files)
            return
        except discord.errors.HTTPException as e:
            pass
        try:
            print("Attempt to chunk files.")
            chunks = pic_list.chunk_image_lists()
            print(f"Uploading {len(chunks)} chunks.")
            for chunk in chunks:
                files = [discord.File(pic) for pic in chunk]
                async with ctx.typing():
                    await ctx.send(files=files)
        except discord.errors.HTTPException as e:
            print(e, file=sys.stdout)
            async with ctx.typing():
                await ctx.send("Command failed due to file size. Try again.")


def setup(bot):
    bot.add_cog(SendPicsCog(bot))


def main():
    return


if __name__ == "__main__":
    main()
