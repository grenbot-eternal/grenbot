#!/usr/bin/env python

"""
Offline script to mimic DWD spreadsheets using EWC webapages

07/09/22
"""

import os
import json
import bs4
import requests
import pandas as pd

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS "
        "X 10_11_5)AppleWebKit/537.36 (KHTML, "
        "like Gecko)Chrome/50.0.2661.102 Safari/537.36"
    )
}


def url_to_bs4(url):
    result = requests.get(url, headers=HEADERS)
    soup = bs4.BeautifulSoup(result.content, "html.parser")
    return soup


def bs4_to_table(soup):
    players = soup.find_all("a", {"class": "text-bold text-lg"})
    return players


def player_to_deck(player):
    player_name = player.contents[0].split("'")[0]
    url_tail = player["href"]
    decklist_url = f"https://eternalwarcry.com/{url_tail}"
    decklist = bs4_to_deck(url_to_bs4(decklist_url))

    deck = decklist.split("\n")

    return player_name, deck


def bs4_to_deck(soup):
    tag = soup.find("textarea", {"id": "export-deck-text"})
    decklist = tag.contents[0]
    return decklist


def bs4_to_cardinfo(soup, setnum):
    imageurl = soup.find("meta", {"property": "og:image"})["content"]
    cardname = os.path.basename(imageurl[:-4]).replace("_", " ")
    out_dict = {
        "SetName": "",
        "SetNumber": setnum,
        "Name": cardname,
        "ImageUrl": imageurl,
    }
    return out_dict


def generate_list(outlist, setnum, range_start, range_end):
    url_stem = "https://eternalwarcry.com/cards/d/"
    for card_id in list(range(range_start, range_end)):
        url = f"{url_stem}/{setnum}-{card_id}/"
        soup = url_to_bs4(url)
        card = bs4_to_cardinfo(soup, setnum)
        if not card["Name"] == "og-image":
            outlist.append(card)


def write_df(dataframe, player_name, fname, mode="a"):
    with pd.ExcelWriter(f"{fname}.xlsx", mode=mode) as writer:
        dataframe.to_excel(writer, sheet_name=player_name, index=False, header=False)


def main():

    url = "https://eternalwarcry.com/tournaments/d/fCmDSvyZtJo/stormbreak-5k-open-throne-top-64"
    fname = url.split("/")[-1]

    soup = url_to_bs4(url)
    player_list = bs4_to_table(soup)

    for player in player_list:
        player_name, deck = player_to_deck(player)
        print(f"Extracting decklist for {player_name}")
        
        df = pd.DataFrame(data=deck, dtype=pd.StringDtype())

        try:
            write_df(df, player_name, fname)
        except FileNotFoundError:
            write_df(df, player_name, fname, "w")


if __name__ == "__main__":
    main()
