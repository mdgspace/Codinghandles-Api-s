from aiohttp import web
import aiohttp_jinja2

async def get_home(request):
    response = aiohttp_jinja2.render_template("home.html", request,{})
    return response