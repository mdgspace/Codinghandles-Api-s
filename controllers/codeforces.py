from aiohttp import web
from services.codeforces import scrapper
import json
import logging 

async def getUser(request):
    handle =  request.match_info['user']
    if not handle:
        return web.Response(status=400, text=f"Missing user parameter")
    try:
        userInfo = await scrapper.get_user_info(handle)
        serialized_data = json.dumps(userInfo.__dict__)
        logging.info(f"Scrapped codeforces userInfo data for {handle}: {serialized_data}")
        return web.Response(status=200, text=serialized_data)
    except Exception as e:
        logging.error("Error: ",e)
        return web.Response(status=404, text="No user found with this handle")
        

async def getContests(request):
   try: 
       contests =  await scrapper.get_upcoming_contests()
       contest_dict_list = [contest.__dict__ for contest in contests]
       serialized_data = json.dumps(contest_dict_list)
       logging.info(f"Codeforces contests scraped: {serialized_data}")
       return web.Response(status=200, text=serialized_data)
   except Exception as e :
       logging.error(f"Error while scraping codeforces future contests: {e}")
       return web.Response(status=500, text="Internal Server Error")


async def getSubmissions(request):
    handle =  request.match_info['user']
    isHandle = await scrapper.checkHandle(handle)
    if  not isHandle:
        return web.Response(status=404, text="User does not exists")
    timestamp = request.query.get('timestamp')
    if timestamp is not None and  not timestamp.isdigit():
        return web.Response(status=400, text="Invalid timestamp provided")
    if timestamp is None:
        timestamp = 0
    else: 
        timestamp = int(timestamp)
    try:
       submissions = await scrapper.get_user_submissions(handle, timestamp)
       submission_dict_list = [submission.__dict__ for submission in submissions]
       serialized_data = json.dumps(submission_dict_list)
       logging.info(f"Codeforces handle {handle} submission scraped: {serialized_data}")
       return web.Response(status=200, text=serialized_data)
    except Exception as e:
        logging.error(f"Error while scrapping submissions : {e}")
        return web.Response(status=500, text="Internal Server Error")


    
    
    


    
