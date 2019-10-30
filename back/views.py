from aiohttp import web
from aiohttp_session import SimpleCookieStorage, session_middleware, get_session
from aiohttp_security import check_permission, \
    is_anonymous, remember, forget, \
    setup as setup_security, SessionIdentityPolicy
from aiohttp_security.abc import AbstractAuthorizationPolicy
import aiohttp_jinja2
import jinja2
import datetime


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

@aiohttp_jinja2.template("/front/creator.html")
async def insert_law(request):
    await check_permission(request, "admin")
    redirect_response = web.HTTPFound('/')
    if request.method == "POST":
        db = request.app.db
        session = await get_session(request)
        form = await request.post()

        print(form)
        title = form.get("title")
        body = form.get("body")
        author = form.get("author")
        date = form.get("date")

        date_in_base = str(datetime.datetime.now())
        editor = session.get("AIOHTTP_SECURITY")

        await db["laws"].insert_one({"title":title,
                                     "body":body,
                                     "author":author,
                                     "date":date,
                                     "date_in_base":date_in_base,
                                     "editor":editor})
        raise redirect_response
    return {}
