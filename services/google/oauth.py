import aiohttp
import os
import json
from dotenv import load_dotenv

load_dotenv()


CLIENT_ID =os.getenv('CLIENT_ID')
CLIENT_SECRET=os.getenv('CLIENT_SECRET')
REDIERECT_URL=os.getenv('REDIERECT_URL')

async def get_token(code):
    url = "https://oauth2.googleapis.com/token"
    data = {
        "code":code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIERECT_URL,
        "grant_type":"authorization_code"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            response_json= await response.json()
            return response_json['access_token']


async def get_user(token):
    url ="https://www.googleapis.com/oauth2/v2/userinfo"
    headers= {
        "Authorization":f"Bearer {token}"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            response_json =  await response.json()
            return response_json
