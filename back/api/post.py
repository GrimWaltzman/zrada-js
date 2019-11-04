from aiohttp import web
import bson.json_util

async def vote(request):
    # TODO: Use Trafaret
    # await check_permission(request, "api")
    try:
        form = await request.json()
        law_id = form["law_id"]
        result = bool(form["accepted"])
    except:
        raise web.HTTPBadRequest

    db = request.app.db

    db["laws"].find_one_and_update({"_id":law_id},
                                   {"accepted": result})
