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

        if not (title and body and author):
            logger.debug("law without fields")
            raise web.HTTPBadRequest()

        number = await db["laws"].find_one(sort=[('_id', -1)])  # find law with max number

        if number and "number" in number:
            number = number["number"] + 1   # increment number
        else:
            number = 1

        date_in_base = str(datetime.datetime.now())
        poster = session.get("AIOHTTP_SECURITY")

        # New law, with one version
        await db["laws"].insert_one({"number": number,
                                     "title": title,
                                     "versions": [
                                         {"version": 1,
                                          "body": body,
                                          "date_in_base":date_in_base,
                                          "author": author,
                                          "poster": poster}],
                                     "author": author,
                                     "date_in_base": date_in_base,
                                     "poster": poster})
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
@aiohttp_jinja2.template("/zrada/law.html")
async def view_law(request):
    await check_permission(request, "view")
    db = request.app.db
    law_number = request.match_info['law']
    logger.debug(law_number)
    try:
        law_number = int(law_number)
    except ValueError:
        raise web.HTTPBadRequest()
    law = await db["laws"].find_one({"number": law_number})
    if law:
        return {"law":law}
    raise web.HTTPNotFound()
