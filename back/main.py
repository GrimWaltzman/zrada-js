from os import getenv
from aiohttp import web
import aiohttp
import asyncio
import aiohttp_jinja2
import jinja2
from aiohttp_session import SimpleCookieStorage, session_middleware
from aiohttp_security import setup as setup_security, SessionIdentityPolicy
from auth.views import SimpleJack_AuthorizationPolicy
from pathlib import Path
from urls import import_urls
from motor.motor_asyncio import AsyncIOMotorClient
from middlewares.custom_exceptions import *

# workaround to add secret
try:
    import secret
except ImportError:
    pass

DEBUG = getenv("CZVLT_DEBUG", "False")
if DEBUG.lower() == "true":
    DEBUG = True
else: # if non "true" value e.g. "false" or bogus string 
    DEBUG = False

loop = asyncio.get_event_loop()

async def db_handler(app, handler):
    async def middleware(request):
        if request.path.startswith('/static/') or request.path.startswith('/_debugtoolbar'):
            response = await handler(request)
            return response

        request.db = app.db
        response = await handler(request)
        return response
    return middleware

HERE = Path(__file__).resolve().parent.parent   # Path app
MONGO_TEMPLATE = "mongodb+srv://admin:{}@quppeq0-qnmoc.mongodb.net/test?retryWrites=true&w=majority"
MONGO_PASSWORD = getenv("MONGO_PASS", "B24v2PLoWJSRcHsc")
MONGO_CONNECT = MONGO_TEMPLATE.format(MONGO_PASSWORD)

#print(MONGO_PASSWORD)



middleware = session_middleware(SimpleCookieStorage())
policy = SessionIdentityPolicy()

exceptions_html = {401: "exceptions/error_401.html"}
exceptions = error_factory(exceptions_html)

app = web.Application(middlewares=[middleware,
                                   db_handler,
                                   exceptions])
app.client = AsyncIOMotorClient(MONGO_CONNECT)
app.db = app.client["zrada"]
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(HERE)+"/front/templates"))
setup_security(app, policy, SimpleJack_AuthorizationPolicy(app.db))


if DEBUG:
    app.add_routes([web.static('/static', str(HERE) + "/front/static", show_index=True),
                    web.static('/avatars', str(HERE) + "/front/avatars", show_index=True)])




import_urls(app)    # Installing routes




async def shutdown(app):
    print("END")

    await app.client.close()  # database connection close
    await app.shutdown()
    await app.cleanup()


try:
    web.run_app(app, port=1488)

finally:
    print("stopped")
    # loop.create_task(shutdown(app))
    loop.close()