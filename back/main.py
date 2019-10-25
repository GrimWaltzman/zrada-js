from aiohttp import web
import aiohttp
import aiohttp_jinja2
import jinja2
from pathlib import Path

here = Path(__file__).resolve().parent.parent
print(here)
@aiohttp_jinja2.template('/front/index.html')
async def hello(request):
    return {}


app= web.Application() # type: web.Application
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(here)))
app.add_routes([web.get('/', hello)])

web.run_app(app, port=1488)