from aiohttp import web
import aiohttp_jinja2
from middlerwares.ip_block import ip_block_middleware

async def get_home(request):
    response = aiohttp_jinja2.render_template("home.html", request,{})
    return response