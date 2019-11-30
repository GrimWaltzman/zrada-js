from aiohttp import web
from aiohttp_session import get_session
from aiohttp_security import check_permission, \
    is_anonymous, remember, forget, \
    setup as setup_security, SessionIdentityPolicy
import aiohttp_jinja2
import jinja2
import datetime


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
        number = form.get("number")
        print(form)

        date_in_base = str(datetime.datetime.now())
        editor = session.get("AIOHTTP_SECURITY")
        print(number)
        print(type(number))

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

async def view_law(request):
    return {}