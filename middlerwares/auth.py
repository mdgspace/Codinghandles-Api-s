from aiohttp import web
import logging
from services.google.oauth import get_user



async def auth_middlerware(request):
    token = request.headers.get('acess_token')
    if not token:
        return web.Response(status=401, text="Unauthorized request")
    try:
       user = await get_user(token)
    except Exception as e:
       return web.Response(status=401, text="Unauthorised request")