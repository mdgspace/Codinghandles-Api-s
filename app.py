from aiohttp import web 
from routes import routes
import jinja2
import aiohttp_jinja2
import  os

app = web.Application() 

aiohttp_jinja2.setup(
    app, loader=jinja2.FileSystemLoader(os.path.join(os.getcwd(), "templates"))
)

router = app.router

routes.setup_routes(router)

web.run_app(app,host='0.0.0.0', port=8080)

if __name__ == '__main__': 
    web.run_app(app)