from aiohttp import web 
from routes import routes
import jinja2
import aiohttp_jinja2
import  os
import aiohttp_cors 
import aioredis
import logging
from dotenv import load_dotenv
from middlerwares.auth import auth_middlerware
from middlerwares.ip_block import ip_block_middleware

load_dotenv()

async def on_startup(app):
    try:
      # Connect to Redis
      url = os.getenv('REDIS_URL')
      app['redis'] = await aioredis.from_url(url)
      logging.info("Redis connected")
    except Exception as e:
        logging.error(f"Could not connect to redis: {e}")
        

async def on_cleanup(app):
    # Close the Redis connection
    app['redis'].close()
    await app['redis'].wait_closed()


app = web.Application() 

app.on_startup.append(on_startup)
app.on_cleanup.append(on_cleanup)
app.middlewares.append(ip_block_middleware)
app.middlewares.append(auth_middlerware)

aiohttp_jinja2.setup(
    app, loader=jinja2.FileSystemLoader(os.path.join(os.getcwd(), "templates"))
)


cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            allow_methods="*",
        )
})

router = app.router

routes.setup_routes(router)

# Configure CORS on all routes.
for route in list(app.router.routes()):
    cors.add(route)

web.run_app(app,host='0.0.0.0', port=8080)


if __name__ == '__main__': 
    web.run_app(app)