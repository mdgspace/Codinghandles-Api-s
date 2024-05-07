from services.leetcode.utils import graphql
from models.userInfo import LeetcodeUserInfo
from models.submission import LeetcodeACSubmission
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc 





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

    

