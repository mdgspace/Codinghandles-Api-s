from aiohttp import web
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
       if user is None:
           return web.Response(status=401, text="Unauthorised request")
    except Exception as e:
       return web.Response(status=500, text="Internal Server Error")
    response = await handler(request)
    return response