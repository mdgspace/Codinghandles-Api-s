from middlerwares.ip_block import ip_block_middleware
from middlerwares.auth import auth_middlerware
from aiohttp import web
from services.codeforces import scrapper
import json
import logging 

async def getUser(request):
    await ip_block_middleware(request)
    await auth_middlerware(request)
    handle =  request.query.get('user')
    if not handle:
        return web.Response(status=400, text=f"Missing user parameter")
    try:
        userInfo = await scrapper.get_user_info(handle)
        serialized_data = json.dumps(userInfo.__dict__)
        return web.Response(status=200, text=serialized_data)
    except Exception as e:
        logging.error("Error: ",e)
        return web.Response(status=404, text="No user found with this handle")
        

# async def getContests(request):
#     print("hello")
