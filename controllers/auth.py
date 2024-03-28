from  aiohttp import web
import os
from dotenv import load_dotenv
import logging
from services.google import oauth
import aiohttp_jinja2
from middlerwares.ip_block import ip_block_middleware
load_dotenv()

CLIENT_ID =os.getenv('CLIENT_ID')
CLIENT_SECRET=os.getenv('CLIENT_SECRET')
REDIERECT_URL=os.getenv('REDIERECT_URL')

async def login(request):
    authUrl= f'https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIERECT_URL}&scope=email profile'
    return web.HTTPFound(authUrl)

async def callback(request):
    code = request.query.get('code')
    try:
        access_token = await oauth.get_token(code)
        user = await oauth.get_user(access_token)
        user_email =  user["email"]
        context = {
            "access_token" : access_token,
            "email" : user_email
        }
        logging.info(f"Account with email: {user_email} registered")
        response = aiohttp_jinja2.render_template("token.html", request, context)
        return response
    except Exception as e:
        logging.error(f"Error : {e}")
        response = aiohttp_jinja2.render_template("error.html", request, {})
        return response
   
    
