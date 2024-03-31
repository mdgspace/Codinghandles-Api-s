from bs4 import BeautifulSoup
from services.codeshef.utils import fetch_url, get_unix_time, get_submission_problem_unixtime, is_more_submissions
import aiohttp
import re
from models.userInfo import CodeshefUserInfo
from models.contest import CodeshefContestInfo
from models.submission import  CodeshefSubmission
import undetected_chromedriver as uc 
from selenium_stealth import stealth
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



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
        return 200, CodeshefUserInfo(handle=handle, rating=int(rating),maxRating=int(maxRating),stars=starsCount,status=status)
    except Exception as e:
        return 404, "User not found"
    

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

            
async def get_user_submissions(handle: str, timestamp: int):
    options = uc.ChromeOptions()
    options.headless = False 
    options.add_argument("--blink-settings=imagesEnabled=false")

    driver = uc.Chrome(use_subprocess=True, options=options)
    wait = WebDriverWait(driver, 10)
    stealth(
    driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
    )
    url = f"https://www.codechef.com/users/{handle}"
    driver.get(url)
    time.sleep(2)
    submissions = []
    while(True):
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('table', class_="dataTable")
        tr_tags = table.find_all('tr')
        tr_tags.pop(0)
        whileBreak = False
        for tr in tr_tags:
            problemTime = tr.find_all('span')[1]
            unix_time = get_submission_problem_unixtime(problemTime.text.strip())

            if unix_time <= timestamp:
                whileBreak = True
                break 
            problemCode = tr.find_all('a')[0].text.strip()
            status = tr.find_all('span')[2]
            status=status.attrs.get('title')
            language= tr.find_all('td')[-2].text.strip()
            submissionData = CodeshefSubmission(problemCode, unix_time, status, language)
            submissions.append(submissionData)
        if(whileBreak):
            break
        pageInfo = soup.find('div', class_="pageinfo").text.strip()
        if not is_more_submissions(pageInfo):
             break  
        driver.execute_script("onload_getpage_recent_activity_user('next');")
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.pageinfo")))
    
    driver.quit()
    return  submissions










            





    

