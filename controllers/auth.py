from  aiohttp import web
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID =os.getenv('CLIENT_ID')
CLIENT_SECRET=os.getenv('CLIENT_SECRET')
REDIERECT_URL=os.getenv('REDIERECT_URL')

async def login(request):
    authUrl= f'https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIERECT_URL}&scope=email profile'
    return web.HTTPFound(authUrl)

async def callback(request):
    code = request.query.get('code')
    return web.Response(text=code)

