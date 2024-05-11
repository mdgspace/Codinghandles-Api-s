import aiohttp
import datetime

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


