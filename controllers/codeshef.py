from aiohttp import web
from services.codeshef import scrapper
import json
import logging 

async def getUser(request):
    handle = request.match_info['user']
    try:
        userInfo = await scrapper.get_user_info(handle)
        serialized_data = json.dumps(userInfo.__dict__)
        logging.info(f"Scrapped codeshef userInfo data for {handle}: {serialized_data}")
        return web.Response(status=200, text=serialized_data)
    except Exception as e:
        logging.error("Error: ",e)
        return web.Response(status=404, text="No user found with this handle")
        

async def getContests(request):
    try:
        contests = await scrapper.get_upcoming_contests()
        contest_dict_list = [contest.__dict__ for contest in contests]
        serialized_data = json.dumps(contest_dict_list)
        return web.Response(status=200, text=serialized_data)
    except Exception as e:
        logging.error("Error with codeshef contests api :", e)
        return web.Response(status=500, text="Internal Server Error")