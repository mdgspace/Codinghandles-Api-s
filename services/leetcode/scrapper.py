import utils
from models.userInfo import LeetcodeUserInfo
from models.submission import LeetcodeACSubmission
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
    user  = await utils.graphql(query, variables, operation)
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
    variables = {"username": handle, "limit": 100}
    submissions = await utils.graphql(query, variables, "recentAcSubmissions")
    submissionsList = []
    if submissions!=None :
        for sub in submissions["recentAcSubmissionList"]:
            if int(sub["1712992296"])>timestamp:
                subObject = LeetcodeACSubmission(problemName=sub["title"], problemSlug=sub["titleSlug"], time=int(sub["1712992296"]))
                submissionsList.append(subObject)
            else:
                break 
            
        return submissionsList
    return None

    




