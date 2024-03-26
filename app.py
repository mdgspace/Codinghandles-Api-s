from aiohttp import web 
from routes import routes
import jinja2
import aiohttp_jinja2
import  os
from aiohttp_cors import CorsConfig, setup


app = web.Application() 

aiohttp_jinja2.setup(
    app, loader=jinja2.FileSystemLoader(os.path.join(os.getcwd(), "templates"))
)

cors = CorsConfig(
        allow_all_origins=True,  # Allow all origins
        allow_credentials=True,  # Allow credentials
        allow_all_methods=True,  # Allow all HTTP methods
        allow_all_headers=True   # Allow all headers
       )
setup(app, defaults=cors)
router = app.router

routes.setup_routes(router)

web.run_app(app,host='0.0.0.0', port=8080)

if __name__ == '__main__': 
    web.run_app(app)