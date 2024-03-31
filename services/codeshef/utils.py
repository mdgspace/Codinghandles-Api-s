import aiohttp
import cloudscraper
from datetime import datetime, timedelta
import re

async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        scraper = cloudscraper.create_scraper(delay=10, browser="chrome") 
        content =  scraper.get(url) 
        return content.text

def get_unix_time(time: str):
    timestamp = datetime.fromisoformat(time)
    unix_time = timestamp.timestamp()
    return int(unix_time)


def get_submission_problem_unixtime(time: str):
    datetime_obj = datetime.strptime(time, "%I:%M %p %d/%m/%y")
    ist_offset = timedelta(hours=5, minutes=30)

    # Adjust the datetime object to IST timezone
    datetime_ist = datetime_obj + ist_offset

    # Convert the datetime object to UNIX time
    unix_time = int(datetime_ist.timestamp())
    return unix_time

# pageinfo ex:"2 of 12"
def is_more_submissions(pageInfo: str):
    numbers = re.findall(r'\d+', pageInfo)
    numbers = [int(num) for num in numbers]
    if numbers[0] != numbers[1]:
        return True
    return False
