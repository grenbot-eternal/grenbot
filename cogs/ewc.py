#!/usr/bin/env python

"""
Offline script to be run to generate a temporary json for missing cards.
Change setnum in the main, and the list range as appropriate.
The json file will not contain any 404 images from ewc.

Move the generated json file to the same location as the eternal-cards.json
to have the cards viewable by the bot.

!update_set can then be used to add the missing images

07/09/22
"""

import os
import json
import bs4
import requests

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


def bs4_to_deck(soup):
    tag = soup.find("textarea", {"id": "export-deck-text"})
    decklist = tag.contents[0]
    return decklist


def bs4_to_cardinfo(soup, setnum):
    imageurl = soup.find("meta", {"property": "og:image"})["content"]
    cardname = os.path.basename(imageurl[:-4]).replace("_", " ")
    out_dict = {"SetName": "", "SetNumber": setnum, "Name": cardname, "ImageUrl": imageurl}
    return out_dict


def generate_list(setnum, range_start, range_end):
    outlist = []
    url_stem = "https://eternalwarcry.com/cards/d/"
    for card_id in list(range(range_start, range_end)):
        url = f"{url_stem}/{setnum}-{card_id}/"
        soup = url_to_bs4(url)
        card = bs4_to_cardinfo(soup, setnum)
        if not card["Name"] == "og-image":
            print(f"Adding {card['Name']}")
            outlist.append(card)
    return outlist


def main():

    output = []
    #generate_list(output, 1135, 1, 28)
    output += generate_list(15, 498, 515)
    output += generate_list(15, 551, 600)
    output += generate_list(1145, 0, 35)

    with open("temp-cards.json", "w", encoding="utf-8") as writer:
        json.dump(output, writer, indent=4)


if __name__ == "__main__":
    main()
