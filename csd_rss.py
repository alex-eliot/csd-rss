import asyncio
import aiohttp
from bs4 import BeautifulSoup
import html
import re
import json
import requests

from github_operations import updateHistory, get_repo

global url
global headers

url = "https://www.csd.auth.gr/category/announcements/"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.47"
}

async def initial_setup(key: str) -> None:
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                html_content = await resp.read()
                rss = parse(html_content)
                updateHistory(get_repo(key), "csd_rss.json", rss)


async def get_new_announcements(key: str) -> tuple:
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                html_content = await resp.read()
                rss = parse(html_content)

                feed_saved = requests.get("https://github.com/alex-eliot/csd-rss/raw/master/csd_rss.json")

                if feed_saved.status_code != 200:
                    await initial_setup(key)
                    return await get_new_announcements(key)
                
                feed_saved = json.loads(feed_saved.text)

                    
                new = []

                for item in rss["feed"]:
                    if item not in feed_saved:
                        new.append(item)
                        feed_saved.append(item)

                updateHistory(get_repo(key), "csd_rss.json", feed_saved)

    return feed_saved, new

def parseDate(inpt: str) -> str:
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

async def parse(inpt: str) -> list:
    soup = BeautifulSoup(inpt, "html.parser")

    posts = soup.find("article")    

    feed = []

    for post in posts:
        post_title = post.find("a").get_text()
        post_link = post.find("a")["href"]
        post_pubDate = post.find("div", {"class": "post-date"}).get_text()
        
        feed.append(
            {
                "title": post_title,
                "link": post_link,
                "pubDate": post_pubDate,
            }
        )

    return feed

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    a = loop.run_until_complete(initial_setup(input("Input decoding key: ")))
    print(a)