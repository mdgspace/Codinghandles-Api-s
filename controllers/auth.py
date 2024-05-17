from  aiohttp import web
import logging
from services.google import oauth
import json


async def login(request):
    code = request.query.get('code')
    if code is None:
        return web.Response(status=404, text="No code provided")
    try:
        access_token = await oauth.get_token(code)
        if access_token is None:
            return web.Response(status=401, text="Invalid code provided")
        user = await oauth.get_user(access_token)
        user_email =  user["email"]
        data = {
            "access_token" : access_token,
            "email" : user_email
        }
        serialized_data = json.dumps(data.__dict__)
        logging.info(f"Account with email: {user_email} registered")
        return web.Response(status=200, text=serialized_data)
    except Exception as e:
        logging.error(f"Error : {e}")
        return web.Response(status=500, text="Internal Server Error")

   
    
