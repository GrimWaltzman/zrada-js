from aiohttp import web
import bson.json_util
import motor.core
from aiohttp_security import permits


async def laws(request):
    # TODO: Use Trafaret
    # await check_permission(request, "api")
    try:
        form = await request.json()
    except:
        form = {}
    limit = form["limit"] if "limit" in form else 10
    skip = form["skip"] if "skip" in form else 0

    token = {"token":form["token"]} if "token" in form else None
    allowed = await permits(request, "api", token)
    if not allowed:
        raise web.HTTPForbidden()

    db = request.app.db
    laws = []
    async for law in db["laws"].find().skip(skip).limit(limit):
        laws.append(law)
    return web.json_response(laws, dumps=bson.json_util.dumps)


async def law(request):

    try:
        form = await request.json()
        law_id = bson.ObjectId(form["_id"])
    except:
        raise web.HTTPBadRequest

    token = {"token": form["token"]} if "token" in form else None
    allowed = await permits(request, "api", token)
    if not allowed:
        raise web.HTTPForbidden()

    db = request.app.db
    law = await db["laws"].find_one({"_id": law_id})
    return web.json_response(law, dumps=bson.json_util.dumps)
