import logging 
from aiohttp import web
from services.leetcode import scrapper
import json

async def getUser(request):
    handle =  request.match_info['user']
    try:
        userInfo = await scrapper.get_user_info(handle)
        if userInfo != None:
            serialized_data = json.dumps(userInfo.__dict__)
            return web.Response(status=200, text=serialized_data)
        return web.Response(status=404, text="No user found with this handle")
    except Exception as e:
        logging.error("Error:",e)
        return web.Response(status=500, text="Internal Server Error")

async def getSubmissions(request):
    handle = request.match_info['user']
    timestamp = request.query.get('timestamp')
    if timestamp is not None and  not timestamp.isdigit():
        return web.Response(status=400, text="Invalid timestamp provided")
    if timestamp is None:
        timestamp = 0
    else:
        timestamp= int(timestamp)
    try:
        submissions =  await scrapper.get_user_submissions(handle, timestamp)
        if submissions is None:
            return web.Response(status=404, text="No user found with this handle")
        submission_dict_list = [submission.__dict__ for submission in submissions]
        serialized_data = json.dumps(submission_dict_list)
        return web.Response(status=200, text=serialized_data)
    except Exception as e:
        logging.error("Error:",e)
        return web.Response(status=500, text="Internal Server Error")



        
        