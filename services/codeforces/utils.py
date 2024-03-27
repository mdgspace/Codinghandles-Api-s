from aiohttp_requests import requests
import aiohttp
from datetime import datetime, timedelta

async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        response = await session.get( url)
        return await response.text()


def get_unix_time(time):
    date_format = "%b/%d/%Y %H:%M"
    dt_object = datetime.strptime(time, date_format)
    utc_offset_hours = 5
    utc_offset_minutes = 30
    utc_offset = timedelta(hours=utc_offset_hours, minutes=utc_offset_minutes)
    dt_object_with_offset = dt_object + utc_offset
    unix_timestamp = dt_object_with_offset.timestamp()    
    return int(unix_timestamp)