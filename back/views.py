import datetime

import aiohttp_jinja2
from aiohttp import web
from aiohttp_security import check_permission, \
    is_anonymous
from aiohttp_session import get_session
import logging

logger = logging.getLogger("views")


@aiohttp_jinja2.template('/zrada/index.html')
async def handler_root(request):
    is_logged = not await is_anonymous(request)
    if is_logged:
        session = await get_session(request)
        mail = session["AIOHTTP_SECURITY"]
    else:
        mail = "not"
    return {"login": mail}


@aiohttp_jinja2.template('/zrada/counter.html')
async def index(request):
    await check_permission(request, "vote")
    db = request.app.db
    laws = []
    async for law in db["laws"].find():
        laws.append(law)
    return {"laws": laws}


@aiohttp_jinja2.template("/zrada/creator.html")
async def insert_law(request):
    await check_permission(request, "admin")
    redirect_response = web.HTTPFound('/')
    if request.method == "POST":
        db = request.app.db
        session = await get_session(request)
        form = await request.json()

        title = form.get("title")
        body = form.get("body")
        author = form.get("author")
        date = form.get("date")
        number = await db["laws"].find_one(sort=[('_id', -1)])  # find law with max number
        number = number["number"] + 1   # increment number


        date_in_base = str(datetime.datetime.now())
        editor = session.get("AIOHTTP_SECURITY")

        await db["laws"].insert_one({"number":number,
                                     "title":title,
                                     "body":body,
                                     "author":author,
                                     "date":date,
                                     "date_in_base":date_in_base,
                                     "editor":editor})
        raise web.HTTPOk(body="Законопроект успішно внесено в базу!")
    return {}


@aiohttp_jinja2.template("/zrada/list_of_laws.html")
async def view_laws(request):
    await check_permission(request, "view")
    db = request.app.db
    laws = []
    async for law in db["laws"].find():
        laws.append(law)
    return {"laws":laws}


# TODO: return law
# request {"id" : id}
# response {"id" : id, "title : title, .. and etc}
async def view_law(request):
    raise web.HTTPNotImplemented()
