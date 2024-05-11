from services.interviewbit.utils import fetch_url
from models.userInfo import InterviewbitUserInfo

async def get_user_info(handle: str):
    userUrl = "https://www.interviewbit.com/v2/profile/username?id="+handle
    userInfo = await fetch_url(userUrl)
    if userInfo is None:
        return None
    worldRank = userInfo["global_rank"]
    submissionUrl = "https://www.interviewbit.com/v2/profile/username/submission-analysis/?id="+handle
    submissionRes = await fetch_url(submissionUrl)
    accuracy = 0
    totalSolved = 0  
    if submissionRes is not None:
        sum=0
        for sub in submissionRes:
            count= sub["count"]
            sum+= int(count)
            if sub["result"] == "correct_answer":
                totalSolved = count
    if totalSolved is not 0:
        accuracy = (totalSolved*100)/sum 
    userObject = InterviewbitUserInfo(handle=handle, worldRank=int(worldRank), accuracy=accuracy, totalSolved=totalSolved)
    return userObject


# https://www.interviewbit.com/v2/profile/username/daily-user-submissions/2024/?id=monarch-s-empire    
# async def get_submissions(handle: str, timestamp: int):

 


    

    
