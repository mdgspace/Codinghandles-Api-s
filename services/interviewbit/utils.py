import aiohttp
from datetime import datetime
import cloudscraper
import re
import pytz


async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                res= await response.json()
                return res
            return None
        

def dateToUnix(date_string):
    date_object = datetime.datetime.strptime(date_string, "%Y-%m-%d")
    unix_time = date_object.timestamp()
    return int(unix_time)

async def scrape_url(url):
    async with aiohttp.ClientSession() as session:
        scraper = cloudscraper.create_scraper(delay=10, browser="chrome") 
        content =  scraper.get(url) 
        return content.text


def contestStartTimeToUnix(date_string):
    # Define the format of the date and time string
    if "IST" in date_string:
        date_format = "%d %b %Y %I:%M %p %Z"
        date_time_obj = datetime.strptime(date_string, date_format)
        time_zone = pytz.timezone('Asia/Kolkata')
        date_time_obj = time_zone.localize(date_time_obj)
        unix_time = int(date_time_obj.timestamp())
        return unix_time
    date_format = "%d %b %Y %I:%M %p %z"
    date_time_obj = datetime.strptime(date_string, date_format)
    unix_time = date_time_obj.timestamp()
    return int(unix_time)

def durationToSeconds(duration_string):
    pattern = r'(\d+)\s*hours\s*(\d+)\s*mins'
    match = re.match(pattern, duration_string)
    if match:
      hours = int(match.group(1))
      minutes = int(match.group(2))
      seconds = (hours * 3600) + (minutes * 60)
      return seconds
    else:
       return 0
 
