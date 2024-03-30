
from bs4 import  BeautifulSoup
from services.codeforces.utils import fetch_url, get_unix_time, fetch_userInfo
from models.userInfo import CodeforceUserInfo
from models.contest import CodeforcesContestInfo
from models.submission import CodeforcesSubmission
import asyncio

async def get_user_info(handle: str):
    for _ in range(3) :
        userRes = await fetch_userInfo(handle)
        if userRes == None:
            await asyncio.sleep(10)
            continue
        elif userRes.get('error')  is None:
            userInfo = CodeforceUserInfo(handle=handle,rating=int(userRes.get('rating')), maxRating=int(userRes.get('maxRating')), status=userRes.get('rank'))
            return 200,userInfo
        else:
            return 404,"No user with this handle"
    return 500, "Internal Server Error"


async def get_upcoming_contests():
    url="https://codeforces.com/contests/page/1"
    html = await fetch_url(url)
    soup = BeautifulSoup(html,"html.parser")
    tbody  =  soup.select('tbody')[0]
    trs = soup.select('tr')
    trs.pop(0)
    trs.pop(0)
    contests = []
    for tr in trs:
        tds = tr.select('td')
        if len(tds) < 1:
            break 
        name = tds[0].text.strip()
        length = tds[3].text.strip()
        time = tds[2].find('span').text.strip()
        unix_time = get_unix_time(time)
        contest = CodeforcesContestInfo(name=name, length=length, time=unix_time)
        contests.append(contest)
    return contests


async def checkHandle(handle: str):
    try:
        url = f"https://codeforces.com/profile/{handle}"
        html = await fetch_url(url)
        soup = BeautifulSoup(html, "html.parser")
        rating = soup.select("span")
        current_rating = rating[17].text.strip()
        status= rating[18].text.strip()
        max_rating = rating[21].text.strip()
        return True
    except Exception as e:
        print(e)
        return False


async def get_user_submissions(handle: str, timestamp :int):
    pageCount = 1
    submission_list = []
    whileBreak = False
    while True:
        if whileBreak:
            break
        url = f"https://codeforces.com/submissions/{handle}/page/{pageCount}"
        html = await fetch_url(url)
        soup = BeautifulSoup(html, "html.parser")
        submissions= soup.find_all("tr")
        del submissions[0]
        submissions.pop()
        time = submissions[0].select('span.format-time')[0].text.strip()
        unix_time= get_unix_time(time)
        if unix_time <= timestamp:
                whileBreak = True
                break
        if len(submission_list) > 0:
            lastSubTime = submission_list[-1].time
            if lastSubTime <= unix_time :
                whileBreak = True
                break 
        for submission in submissions:
            time = submission.select('span.format-time')[0].text.strip()
            unix_time= get_unix_time(time)
            if unix_time <= timestamp:
                break
            if len(submission_list) > 0:
               lastSubTime = submission_list[-1].time
               if lastSubTime <= unix_time :
                   break 
            
            submission_verdict_wrapper = soup.find('span', class_='submissionVerdictWrapper')
            submission_verdict = submission_verdict_wrapper['submissionverdict']
            timeconsumed =submission.find('td', class_="time-consumed-cell").text.strip()
            spaceconsumed = submission.find('td', class_= "memory-consumed-cell").text.strip()
            problem_title = submission.find_all('td', class_='status-small')[1]
            problem= problem_title.find('a').text.strip().split(' - ')[1]
            problem_code_href = problem_title.find('a')['href']
            parts =problem_code_href.split('/')
            problem_code = f"{parts[2]}-{parts[4]}"
            
            language = submission.select('td:not([class])')[0].text.strip()
            submission_object = CodeforcesSubmission(problemCode=problem_code, problemName=problem, time = unix_time, language=language, status=submission_verdict, timeConsumed=timeconsumed, spaceConsumed=spaceconsumed)
            submission_list.append(submission_object)
        pageCount+=1
        
    return submission_list
    
    
    

