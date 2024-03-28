from middlerwares.ip_block import ip_block_middleware
from middlerwares.auth import auth_middlerware
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
        
