import aiohttp
import cloudscraper
from datetime import datetime

async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        scraper = cloudscraper.create_scraper(delay=10, browser="chrome") 
        content =  scraper.get(url) 
        return content.text

def get_unix_time(time: str):
    timestamp = datetime.fromisoformat(time)
    unix_time = timestamp.timestamp()
    return int(unix_time)
