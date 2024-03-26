from aiohttp import web
import logging


async def ip_block_middleware(request):
    redis =  request.app['redis']
    key = request.remote + ':' + request.path
    client_ip = request.remote
    if await redis.exists(client_ip):
        return web.Response(status=403, text="You are blocked")
    if await redis.exists(key):
        if  int(await redis.get(key)) > 100 :
           logging.info(f"ip_address: {client_ip} blocked for one day")
           await redis.setex(client_ip, 86400, 1)
           return web.Response(status=403, text="Rate limit exeeded")
        await redis.incr(key)
    else:
        await redis.setex(key, 60, 1) 
    
    
    

    
    

    

    
    
