import discord
import asyncio
import urllib.parse
import io
import os
import json
import base64

import csd_rss
from github_operations import updateHistory, get_repo

bot_owner = 242634160026550274
client = discord.Client()

async def refresh() -> None:
    default_csd, new_csd = await csd_rss.get_new_announcements(key)
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
                    "text": "Δημοσιεύτηκε από {}".format(entry["creator"])
                },
                "timestamp": entry["pubDate"],
                "thumbnail": {
                    "url": default_csd["favicon"]
                }
            }

            channel = client.get_channel(854856660932624434)
            await channel.send(embed=discord.Embed.from_dict(embed_dict))
            updateHistory(get_repo(key), "csd_rss.json", default_csd)

@client.event
async def on_ready() -> None:
    channel = client.get_channel(854856660932624434)
    await channel.send("Process initiated.")
    while True:
        await refresh()
        await asyncio.sleep((1 * 60) * 5) # 5 minutes

@client.event
async def on_message(message) -> None:
    if message.content.startswith("="):
        if message.content == "=ping":
            await message.channel.send("Ping back.")

def start():
    with io.open("tokens.json", mode="r", encoding="utf-8") as f:
        global key
        key = os.getenv("key")
        if not key:
            key = input("Input key: ")

        tokens = json.load(f)

        discord_token_encoded = tokens["discord_token"]
        discord_token_decoded = "".join(tuple([chr(ord(discord_token_encoded[i]) ^ ord(key[i % len(key)])) for i in range(len(discord_token_encoded))]))

        client.run(base64.b64decode(discord_token_decoded).decode("utf-8"))

if __name__ == "__main__":
    start()