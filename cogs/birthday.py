#!/usr/bin/env python

import os
import random
from datetime import datetime, timedelta, timezone

from discord.ext import commands

from .constants import CHANNELS, TIMEZONE_DELTA, PIC_DIR
from .utils import filter_input, in_channel

BIRTHDAYS = {
    "0101": [["gugudan", "mimi"]],
    "0601": [["clc", "eunbin"]],
    "0701": [
        ["dreamcatcher", "yoohyeon"],
        ["fromis9", "saerom"],
        ["wekimeki", "sei"],
    ],
    "1001": [["exid", "solji"], ["wjsn", "yeoreum"]],
    "1101": [["izone", "chaeyeon"]],
    "2201": [["momoland", "daisy"], ["fromis9", "seoyeon"]],
    "2501": [["oh my girl", "seunghee"]],
    "2601": [["wjsn", "xuanyi"]],
    "3101": [["g-idle", "miyeon"]],
    "0102": [["twice", "jihyo"]],
    "0302": [["dreamcatcher", "gahyeon"]],
    "1002": [["loona", "kim_lip"]],
    "1102": [["lovelyz", "jisoo"]],
    "2102": [["red velvet", "wendy"]],
    "0303": [["apink", "chorong"]],
    "0603": [["wjsn", "lewda"]],
    "0703": [["dreamcatcher", "dami"]],
    "1703": [["rocket punch", "suyun"]],
    "2003": [["lovelyz", "kei"], ["fromis9", "jiwon"]],
    "2403": [["twice", "mina"]],
    "2603": [["dreamcatcher", "handong"]],
    "2703": [["blackpink", "lisa"]],
    "2903": [["red velvet", "irene"]],
    "0404": [["oh my girl", "jiho"]],
    "1504": [["apink", "namjoo"]],
    "1604": [["wjsn", "dawon"]],
    "1704": [["itzy", "ryujin"], ["fromis9", "jiheon"]],
    "2004": [["wekimeki", "suyeon"]],
    "2304": [["twice", "chaeyoung"]],
    "3004": [["gugudan", "hana"]],
    "0105": [["exid", "hani"], ["oh my girl", "mimi"]],
    "0805": [["exid", "jeonghwa"]],
    "1305": [["girl's day", "minah"]],
    "1405": [["fromis9", "chaeyoung"], ["wjsn", "dayoung"]],
    "1705": [["dreamcatcher", "jiu"]],
    "2405": [["loona", "yves"]],
    "2605": [["dia", "eunchae"], ["itzy", "yeji"]],
    "2705": [["wjsn", "eunseo"]],
    "2805": [["twice", "dubu"]],
    "3005": [["gfriend", "eunha"]],
    "0406": [["lovelyz", "yein"], ["loona", "choerry"]],
    "0506": [["itzy", "chaeryeong"]],
    "0706": [["dia", "jooeun"]],
    "1306": [["loona", "Jinsoul"]],
    "1406": [["twice", "tzuyu"]],
    "1806": [["oh my girl", "arin"], ["izone", "nako"]],
    "0107": [["hinapia", "Eunwoo"]],
    "1307": [["dia", "yebin"]],
    "1507": [["wjsn", "cheng xiao"]],
    "1907": [["apink", "hayoung"]],
    "2007": [["wekimeki", "elly"]],
    "2807": [["oh my girl", "hyojung"]],
    "2907": [["hinapia", "minkyeung"], ["pristin", "roa"]],
    "0108": [["momoland", "yeonwoo"]],
    "0308": [["wjsn", "yeonjung"]],
    "0508": [["gugudan", "hyeyeon"]],
    "1008": [["dreamcatcher", "Sua"], ["clc", "yeeun"]],
    "1208": [["clc", "yujin"]],
    "1308": [["apink", "bomi"]],
    "1408": [["rocket punch", "Sohee"]],
    "1608": [["gugudan", "haebin"]],
    "1808": [["apink", "eunji"]],
    "1908": [["wjsn", "bona"], ["gfriend", "yerin"]],
    "2208": [["Kard", "somin"]],
    "2608": [["g-idle", "soyeon"]],
    "2808": [["gugudan", "sejeong"]],
    "3008": [["caolu"]],
    "3108": [["wekimeki", "lucy"]],
    "0209": [["dia", "eunice"]],
    "0309": [["red velvet", "joy"]],
    "0909": [["oh my girl", "binnie"]],
    "1409": [["dia", "jenny"]],
    "1709": [["oh my girl", "yooa"]],
    "2209": [["hyoyeon"], ["twice", "nayeon"]],
    "2309": [["g-idle", "yuqi"]],
    "2709": [["izone", "eunbi"], ["momoland", "ahin"], ["wekimeki", "rina"]],
    "2909": [["fromis9", "hayoung"], ["izone", "yena"]],
    "0110": [["dreamcatcher", "siyeon"]],
    "0310": [["rocket punch", "Juri"]],
    "0610": [["wekimeki", "lua"]],
    "1010": [["clc", "seunghee"]],
    "1310": [["Hyoseong"]],
    "1510": [["wjsn", "Mei Qi"]],
    "1910": [["loona", "heejin"]],
    "2010": [["Kard", "bm"]],
    "2310": [["gugudan", "sally"], ["g-idle", "minnie"]],
    "0111": [["twice", "Jeongyeon"], ["rocket punch", "Yoonkyung"]],
    "0211": [["clc", "elkie"]],
    "0611": [["wjsn", "exy"], ["clc", "seungyeon"]],
    "1211": [["wekimeki", "yoojung"]],
    "1511": [["loona", "hyunjin"]],
    "1811": [["clc", "sorn"]],
    "1911": [["loona", "gowon"], ["lovelyz", "sujeong"]],
    "2311": [["fromis9", "jisun"]],
    "0112": [["dia", "chaeyeon"]],
    "0412": [["gugudan", "mina"]],
    "0612": [["rocket punch", "Yeonhee"]],
    "0712": [["gfriend", "sowon"]],
    "1012": [["exid", "le"]],
    "2012": [["momoland", "Jane"]],
    "2412": [["wjsn", "seola"]],
    "2712": [["fromis9", "gyuri"]],
    "2912": [["twice", "sana"]],
}


class BirthdayCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def kst_datetime(self):
        return datetime.now(tz=timezone.utc) + TIMEZONE_DELTA

    @in_channel(*CHANNELS)
    @commands.command(
        name="bday",
        help=(
            "Usage: !bday int to post int pics of an idol on their birthday."
            "\nNumber of pics is limited to between 1 and 5."
        ),
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def send_bday_pics(self, ctx, num_pics=1):

        send_pics = self.bot.get_cog("SendPicsCog")
        if send_pics is None:
            await ctx.send("Send pic commands setup failed")
            return

        num_pics = filter_input(num_pics, 1, 5)
        print("Picking idol.")
        date = (self.kst_datetime()).strftime("%d%m")
        try:
            idols = BIRTHDAYS[date]
        except KeyError:
            await ctx.send("No birthdays found for today.")
            return
        idol = random.choice(idols)
        directory = os.path.join(PIC_DIR, *idol)
        await send_pics.async_send_pics(ctx, num_pics, directory)

    @in_channel(*CHANNELS)
    @commands.command(
        name="next_bday",
        help=("Usage: !next_bday to show next day where !bday is valid."),
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def read_next_bday(self, ctx):
        date = self.kst_datetime()
        YYYY = date.year
        for key in BIRTHDAYS:
            key_ddmm = f"{key}{YYYY}"
            key_ddmm = datetime.strptime(key_ddmm, "%d%m%Y").replace(tzinfo=timezone.utc)
            if key_ddmm > date:
                idols = []
                for idol in BIRTHDAYS[key]:
                    idols.append(idol[-1])
                break
        output = key_ddmm.strftime("%d-%m-%Y")
        output = f"Next birthday is on **{output}** for **{', '.join(idols)}**"
        await ctx.send(output)


def setup(bot):
    bot.add_cog(BirthdayCog(bot))


def main():
    # To-do: Add json dump?
    return


if __name__ == "__main__":
    main()
