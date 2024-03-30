from bs4 import BeautifulSoup
from services.codeshef.utils import fetch_url, get_unix_time
import aiohttp
import re
from models.userInfo import CodeshefUserInfo
from models.contest import CodeshefContestInfo

async def get_user_info(handle: str):
    url = f"https://www.codechef.com/users/{handle}"
    html = await fetch_url(url)
    soup = BeautifulSoup(html,'html.parser')
    rating = soup.find('div', class_='rating-number').text.strip()
    maxratingText = soup.find_all('small', class_=False)[-1].text.strip()
    maxRating =re.search(r'\d+', maxratingText).group()
    contentDiv = soup.find_all('div', attrs={'class': ['rating-header', 'text-center']})[0]
    starsSpan = contentDiv.find_all('span')
    starsCount = len(starsSpan)
    status = contentDiv.find_all('div', _class=False)[1].text.strip('()')
    userInfo = CodeshefUserInfo(handle=handle, rating=int(rating),maxRating=int(maxRating),stars=starsCount,status=status)
    return userInfo


async def checkHandle(handle: str):
    try:
        url = f"https://www.codechef.com/users/{handle}"
        html = await fetch_url(url)
        soup = BeautifulSoup(html,'html.parser')
        rating = soup.find('div', class_='rating-number').text.strip()
        maxratingText = soup.find_all('small', class_=False)[-1].text.strip()
        maxRating =re.search(r'\d+', maxratingText).group()
        contentDiv = soup.find_all('div', attrs={'class': ['rating-header', 'text-center']})[0]
        starsSpan = contentDiv.find_all('span')
        starsCount = len(starsSpan)
        status = contentDiv.find_all('div', _class=False)[1].text.strip('()')
        return True 
    except Exception as e:
        return False
    

async def get_upcoming_contests():
    url = "https://www.codechef.com/api/list/contests/all?sort_by=START&sorting_order=asc&offset=0&mode=premium"
    contests = None
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            
            response = await resp.json()
            contests = response['future_contests']
    contestsList = []
    for contest in contests:
        code = contest["contest_code"]
        name = contest["contest_name"]
        length = contest["contest_duration"]
        start_date = contest["contest_start_date_iso"]
        unix_time =get_unix_time(start_date)
        contestData = CodeshefContestInfo(name, code, int(length), unix_time)
        contestsList.append(contestData)
    return contestsList

            

    

