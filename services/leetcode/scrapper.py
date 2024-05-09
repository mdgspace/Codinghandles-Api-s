from services.leetcode.utils import graphql, fetch_url, unix_time
from models.userInfo import LeetcodeUserInfo
from models.submission import LeetcodeACSubmission
from models.contest import LeetcodeContestInfo
from bs4 import BeautifulSoup

async def get_user_info(handle: str):
    query = '''
  query userPublicProfile($username: String!) {
    matchedUser(username: $username) {
      username
      profile {
        ranking
      }
      submitStats {
		acSubmissionNum {
			submissions
		}
		totalSubmissionNum {
			submissions
		}
	  }
    }
  }
'''
    variables = {'username': handle}
    operation= 'userPublicProfile'
    matchedUser  = await graphql(query, variables, operation)
    user= matchedUser["matchedUser"]
    if user != None :
        accuracy=0
        if user["submitStats"]["totalSubmissionNum"][0]['submissions'] != 0:
            accuracy = (user["submitStats"]["acSubmissionNum"][0]['submissions']*1.0/user["submitStats"]["totalSubmissionNum"][0]['submissions'])*100

        accuracy = (user["submitStats"]["acSubmissionNum"][0]['submissions']*1.0/user["submitStats"]["totalSubmissionNum"][0]['submissions'])*100
        userInfo = LeetcodeUserInfo(handle=user['username'], worldRank=int(user['profile']['ranking']), accuracy=int(accuracy))
        return userInfo
    return None



async def get_user_submissions(handle: str, timestamp: int):
    query = '''
    query recentAcSubmissions($username: String!, $limit: Int!) {
      recentAcSubmissionList(username: $username, limit: $limit) {
        id
        title
        titleSlug
        timestamp
      }
    }
'''
    user = await get_user_info(handle)
    if user is None:
        return None
    variables = {"username": handle, "limit": 1000}
    submissions = await graphql(query, variables, "recentAcSubmissions")
    submissionsList = []
    if submissions!=None :
        for sub in submissions["recentAcSubmissionList"]:
            if int(sub["timestamp"])>timestamp:
                subObject = LeetcodeACSubmission(problemName=sub["title"], problemSlug=sub["titleSlug"], time=int(sub["timestamp"]))
                submissionsList.append(subObject)
            else:
                break 
            
        return submissionsList
    return None


async def get_contests():
      ur = "https://leetcode.com/contest/"
      html = await fetch_url(ur)
      soup  =  BeautifulSoup(html, 'html.parser')
      contests = soup.select('a[href^="/contest/"]')
      contestList = []
      for i in range(2):
          name = contests[i].select_one('div.truncate span').text.strip()
          time = contests[i].find_all('div', _class=False)[-1].text.strip()
          # unixTime= unix_time(time)
          contestObject = LeetcodeContestInfo(name=name, time=time)
          contestList.append(contestObject)
      return contestList
      
         


          
      




        

