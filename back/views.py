from aiohttp import web
from aiohttp_session import SimpleCookieStorage, session_middleware, get_session
from aiohttp_security import check_permission, \
    is_anonymous, remember, forget, \
    setup as setup_security, SessionIdentityPolicy
from aiohttp_security.abc import AbstractAuthorizationPolicy
import aiohttp_jinja2
import jinja2



@aiohttp_jinja2.template('/front/index2.html')
async def handler_root(request):
    is_logged = not await is_anonymous(request)
    if is_logged:
        session = await get_session(request)
        mail = session["AIOHTTP_SECURITY"]
    else:
        mail = "not"
    return {"login": mail}





async def handler_listen(request):
    await check_permission(request, 'listen')
    return web.Response(body="I can listen!")


async def handler_speak(request):
    await check_permission(request, 'speak')
    return web.Response(body="I can speak!")

@aiohttp_jinja2.template('/front/counter.html')
async def index(request):
    await check_permission(request, "vote")
    return {}
