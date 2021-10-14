import asyncio
import aiohttp
from bs4 import BeautifulSoup
import io
import html
import re
import json
from datetime import datetime

global url
global headers

url = "https://www.csd.auth.gr/category/announcements/feed"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.47"
}

async def initial_setup():
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                html_content = await resp.read()
                rss = parse(html_content)

                with io.open("csd_rss.json", mode="w", encoding="utf-8") as f:
                    json.dump(rss, f, indent=2)

async def get_new_announcements():
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                html_content = await resp.read()
                rss = parse(html_content)

                with io.open("csd_rss.json", mode="r", encoding="utf-8") as f:
                    rss_saved = json.load(f)

                rss_saved["title"] = rss["title"]
                rss_saved["link"] = rss["link"]
                rss_saved["lastUpdate"] = rss["lastUpdate"]
                rss_saved["favicon"] = rss["favicon"]
                rss_saved["feed"] = []
                    
                new = []

                for item in rss["feed"]:
                    if item not in rss_saved["feed"]:
                        new.append(item)
                        rss_saved["feed"].append(item)

                with io.open("csd_rss.json", mode="w", encoding="utf-8") as f:
                    json.dump(rss_saved, f, indent=2)

    return rss_saved, new

def parseDate(inpt):
    inpt = inpt.split(", ")[1]
    slices = inpt.split(" ")

    months = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12
    }

    time_dict = {
        "DD": slices[0],
        "Mon": months[slices[1]],
        "YYYY": slices[2],
        "TT:TT:TT": slices[3],
        "+TZXX": slices[4]
    }

    return "{}-{}-{}T{}".format(time_dict["YYYY"], time_dict["Mon"], time_dict["DD"], time_dict["TT:TT:TT"])

def parse(inpt):
    soup = BeautifulSoup(inpt, "html.parser")

    channel = soup.rss.channel
    title = channel.title.get_text().replace("&#8211;", "—")
    main_url = "https://www.csd.auth.gr/announcements/"
    lastUpdate = parseDate(channel.lastbuilddate.get_text())

    favicon = channel.url.get_text()
    items = channel.find_all("item")

    feed = []

    for item in items:
        item_title = item.title.get_text()
        item_link = item.comments.get_text().replace("#respond", "")
        item_pubDate = parseDate(item.pubdate.get_text())
        creator = item.find("dc:creator").get_text()

        description_raw = item.description.get_text()
        description_decoded = description_raw
        for entity in re.findall(r'&#[0-9]{4};', description_raw):
            description_decoded = description_decoded.replace(entity, html.unescape(entity))
        
        feed.append(
            {
                "title": item_title,
                "link": item_link,
                "pubDate": item_pubDate,
                "creator": creator,
                "description": description_decoded
            }
        )

    announcements = {
        "title": title,
        "link": main_url,
        "lastUpdate": lastUpdate,
        "favicon": favicon,
        "feed": feed
    }

    return announcements


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    a = loop.run_until_complete(initial_setup())
    print(a)