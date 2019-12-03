import aiohttp_jinja2
from aiohttp import web
from aiohttp_security import remember, forget, \
    check_authorized
from aiohttp_security.abc import AbstractAuthorizationPolicy
from passlib.hash import sha256_crypt


class SimpleJack_AuthorizationPolicy(AbstractAuthorizationPolicy):

    def __init__(self, db):
        self.collection = db["users"]

    async def authorized_userid(self, identity):
        """Retrieve authorized user id.
        Return the user_id of the user identified by the identity
        or 'None' if no user exists related to the identity.
        """
        print(identity)
        if identity:
            return await self.collection.find_one({"login": identity})
        return None

    async def permits(self, identity, permission, context=None):
        """Check user permissions.
        Return True if the identity is allowed the permission
        in the current context, else return False.
        """
        print(context)
        if type(context) == dict and "token" in context:
            user = await self.collection.find_one({"token": context["token"]})
        elif identity:
            user =  await self.collection.find_one({"login": identity})
        else: return False
        print(user)
        if user:
            # TODO: delete legacy   ' "permits" in user  '
            return permission in user["permits"] if "permits" in user else False
        else:
            return False

        # return identity == 'jack' and permission in ('listen',)


async def check_credentials(db, username, password):

    user = await db["users"].find_one({"login": username})

    if user is not None and user["password"]:
        secret = user["password"]
        return sha256_crypt.verify(password, secret)
    return False

@aiohttp_jinja2.template('/auth/login.html')
async def handler_login(request):

    if request.method == "POST":

        redirect_response = web.HTTPFound('/')
        form = await request.post()
        login = form.get('login')
        password = form.get('password')
        db_engine = request.app.db
        if await check_credentials(db_engine, login, password):
            await remember(request, redirect_response, login)
            raise redirect_response
        raise web.HTTPUnauthorized(
            body='Invalid username/password combination')
    return {}

@aiohttp_jinja2.template("/auth/signin.html")
async def handler_signin(request):
    if request.method == "POST":
        redirect_response = web.HTTPFound('/')
        form = await request.post()
        db = request.app.db
        login = form.get('login')
        password = form.get('password')
        hash = sha256_crypt.hash(password)
        await db["users"].insert_one({
            "login": login,
            "password": hash,
            "permits": [
                "view"
            ]})
        raise redirect_response
    return {}




async def handler_logout(request):
    await check_authorized(request)
    redirect_response = web.HTTPFound('/')
    await forget(request, redirect_response)
    raise redirect_response