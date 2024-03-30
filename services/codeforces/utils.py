
import aiohttp
from datetime import datetime, timedelta
import cloudscraper
import logging

async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        scraper = cloudscraper.create_scraper(delay=10, browser="chrome") 
        content =  scraper.get(url) 
        return content.text

async def fetch_userInfo(handle):
    url = f"https://codeforces.com/api/user.info?handles={handle}"
    try:
     async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
           if response.status == 200:
              res = await response.json()
              return res["result"][0]
    except aiohttp.ClientResponseError as e:
       status_code = e.status
       if status_code == 400 :
          return  {"error": "Incorrect handle"}
       else :
          logging.warning("Codeforces userInfo Api failed: ",e)
          return None


def get_unix_time(time):
    date_format = "%b/%d/%Y %H:%M"
    dt_object = datetime.strptime(time, date_format)
    utc_offset_hours = 5
    utc_offset_minutes = 30
    utc_offset = timedelta(hours=utc_offset_hours, minutes=utc_offset_minutes)
    dt_object_with_offset = dt_object + utc_offset
    unix_timestamp = dt_object_with_offset.timestamp()    
    return int(unix_timestamp)