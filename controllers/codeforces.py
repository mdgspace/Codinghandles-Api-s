from aiohttp import web
from services.codeforces import scrapper
import json
import logging 

async def getUser(request):
    handle =  request.match_info['user']
    status, res = await scrapper.get_user_info(handle)
    if status == 200:
       res = json.dumps(res.__dict__)
    return web.Response(status=status, text=res)
    

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
    status, _ = await scrapper.get_user_info(handle)
    if status == 404:
        return web.Response(status=404, text="User does not exists")
    elif status == 500:
        return web.Response(status=500, text="Internal Server Error")
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
        logging.error(f"Error while scrapping codeforces submissions : {e}")
        return web.Response(status=500, text="Internal Server Error")


    
    
    


    
