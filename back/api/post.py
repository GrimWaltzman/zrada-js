import bson.json_util
from aiohttp import web
from aiohttp_security import permits, is_anonymous
import datetime
from aiohttp_session import get_session
import logging
from auth.views import token_user


logger = logging.getLogger("api_post")


async def vote(request):
    # TODO: Use Trafaret
    try:
        form = await request.json()
        law_id = bson.ObjectId(form["_id"])
        result = bool(form["accepted"])
    except Exception:
        raise web.HTTPBadRequest

    token = {"token": form["token"]} if "token" in form else None
    allowed = await permits(request, "api", token)
    if not allowed:
        raise web.HTTPForbidden()

    db = request.app.db

    res = await db["laws"].find_one_and_update(
        {"_id": law_id},
        {"$set": {"accepted": result}})
    logger.info(f"Law with id: {law_id} change status to: {res['accepted']}")

    return web.json_response({"result": "OK"}, dumps=bson.json_util.dumps)


async def law_del(request):
    try:
        form = await request.json()
        law_id = bson.ObjectId(form["_id"])
    except Exception:
        raise web.HTTPBadRequest()

    token = {"token": form["token"]} if "token" in form else None
    allowed = await permits(request, "api", token)
    if not allowed:
        raise web.HTTPForbidden()

    db = request.app.db

    res = await db["laws"].delete_one({"_id": law_id})
    logger.info(f"delete vote: {law_id}")
    return web.json_response({"result": "OK"}, dumps=bson.json_util.dumps)


async def add_version(request):
    try:
        form = await request.json()
        body = form["body"]
        author = form["author"]
        date_in_base = str(datetime.datetime.now())
        law_id = bson.ObjectId(form["_id"])
    except Exception:
        raise web.HTTPBadRequest()

    token = {"token": form["token"]} if "token" in form else None
    allowed = await permits(request, "api", token)
    if not allowed:
        raise web.HTTPForbidden()

    db = request.app.db

    if token:
        poster = await token_user(db, token["token"])
        logger.debug(poster)
        poster = poster["login"]
    else:
        is_logged = not await is_anonymous(request)
        if is_logged:
            session = await get_session(request)
            poster = session["AIOHTTP_SECURITY"]
        else:
            raise web.HTTPConflict()

    law = await db["laws"].find_one({"_id": law_id})  # find law with max number

    if law:
        number = len(law["versions"]) + 1  # increment number
    else:
        raise web.HTTPNotFound()

    version = {"version": number,
               "body": body,
               "date_in_base": date_in_base,
               "author": author,
               "poster": poster}

    res = await db["laws"].update_one({"_id": law_id},{"$push": {"versions":version}})
    logger.info(f"add version: {law_id}")
    return web.json_response({"result": "OK"}, dumps=bson.json_util.dumps)

