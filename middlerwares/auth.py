from aiohttp import web
import logging
from services.google.oauth import get_user


@web.middleware
async def auth_middlerware(request, handler):
    if not request.path.startswith("/api"):
        response = await handler(request)
        return response
    token = request.headers.get('access-token')
    if not token:
        return web.Response(status=401, text="Unauthorized request")
    try:
       user = await get_user(token)
    except Exception as e:
       return web.Response(status=401, text="Unauthorised request")
    response = await handler(request)
    return response