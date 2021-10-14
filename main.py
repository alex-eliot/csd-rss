import discord
import asyncio
import urllib.parse
import io
import json

import csd_rss

bot_owner = 242634160026550274
client = discord.Client()

async def refresh():
    default_csd, new_csd = await csd_rss.get_new_announcements()
    if new_csd:
        for entry in new_csd:
            embed_dict = {
                "title": entry["title"],
                "description": entry["description"],
                "url": urllib.parse.unquote(entry["link"]),
                "color": 1484460,
                "author": {
                    "name": default_csd["title"],
                    "url": urllib.parse.unquote(default_csd["link"])
                },
                "footer": {
                    "text": "Δημοσιεύτηκε"
                },
                "timestamp": entry["pubDate"],
                "thumbnail": {
                    "url": default_csd["favicon"]
                }
            }

        channel = client.get_channel(854856660932624434)
        await channel.send(content="Test", embed=discord.Embed.from_dict(embed_dict))


@client.event
async def on_ready():
    print("Logged in as {}".format(client.user))
    while True:
        await refresh()
        await asyncio.sleep((1 * 60) * 5) # 5 minutes

with io.open("settings.json", mode="r", encoding="utf-8") as f:
    settings = json.load(f)
    
    client.run(settings["token"])