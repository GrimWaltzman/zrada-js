from aiohttp import web
import bson.json_util

async def vote(request):
    # TODO: Use Trafaret
    # await check_permission(request, "api")
    try:
        form = await request.json()
        law_id = bson.ObjectId(form["_id"])
        result = bool(form["accepted"])
    except Exception:
        raise web.HTTPBadRequest

    db = request.app.db

    res = await db["laws"].find_one_and_update({"_id":law_id},
                                   {"accepted": result})
    return web.json_response({"result": "OK"}, dumps=bson.json_util.dumps)

async def law_del(request):
    try:
        form = await request.json()
        law_id = bson.ObjectId(form["_id"])
    except Exception:
        raise web.HTTPBadRequest

    db = request.app.db

    res = await db["laws"].delete_one({"_id": law_id})
    return web.json_response({"result": "OK"}, dumps=bson.json_util.dumps)