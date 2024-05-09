import aiohttp
import cloudscraper
from datetime import datetime, timedelta
import pytz

async def graphql(query, variables, opertation):
    payload= {
        'query':query,
        'operationName': opertation,
        'variables': variables
    }
    async with aiohttp.ClientSession() as session:
        async with session.post('https://leetcode.com/graphql/', json=payload) as response:
            if response.status == 200:
                res= await response.json()
                return res["data"]
            return None
            


async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        scraper = cloudscraper.create_scraper(delay=10, browser="chrome") 
        content =  scraper.get(url) 
        return content.text


def unix_time(target_string):
    target_format = "%A %I:%M %p %Z"
    target_datetime = datetime.strptime(target_string, target_format)
    current_time_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
    days_to_add = (6 - current_time_utc.weekday()) % 7  
    target_datetime += timedelta(days=days_to_add)
    target_datetime = target_datetime.replace(hour=2, minute=30, second=0, microsecond=0)
    unix_time = int(target_datetime.timestamp())
    return unix_time




