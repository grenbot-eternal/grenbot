# Grenbot

Basic discord bot, written using discordpy v2.0.0, for providing eternal card images.

Slash commands are not supported at this release.


## Getting started:

The following changes are required to get the bot to initially run:

```
.env with DISCORD_TOKEN={token_value}
CARD_IMAGES in grenbot changed to provide abs path for where card images are stored.
Local read/write permission to create .json files and card images.
```

## Missing promos:

Sometimes there is a delay between EWC including the promos on its website and updating the .json file the bot uses.

You can use ```python /cogs/ewc.py``` to create a temporary json file of those missing cards, and move that file to the same 
directory as eternal-cards.json.

You can then use the bot commands to download images. When the ewc json is updated you can just delete the temporary file.


## Disclaimer:
Unaffiliated with Eternal, Direwolf Digital or eternalwarcry.com

Please consider supporting [eternalwarcy.com](https://eternalwarcry.com/about/patreon) as this bot
would not be possible without their work.
