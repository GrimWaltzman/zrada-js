import bson.json_util
from aiohttp import web
from aiohttp_security import permits
import logging


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
        raise web.HTTPBadRequest

    token = {"token": form["token"]} if "token" in form else None
    allowed = await permits(request, "api", token)
    if not allowed:
        raise web.HTTPForbidden()

    db = request.app.db

    res = await db["laws"].delete_one({"_id": law_id})
    logger.info(f"delete vote: {law_id}")
    return web.json_response({"result": "OK"}, dumps=bson.json_util.dumps)
