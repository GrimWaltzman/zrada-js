from views import *
from auth.views import *
import api.get
import api.post
from aiohttp import web
def import_urls(app: web.Application):
    app.add_routes([web.get('/', handler_root, name="index"),
        web.get('/login', handler_login, name="login"),
        web.post('/login', handler_login, name="login"),
        web.get('/signin', handler_signin, name="signin"),
        web.post('/signin', handler_signin, name="signin"),
        web.get('/logout', handler_logout, name="logout"),
        web.get('/vote', index, name="vote"),
        web.get('/insert_law', insert_law, name="insert_law"),
        web.post('/insert_law', insert_law, name="insert_law"),
        web.get('/laws', view_laws, name="view_laws"),
        web.get(r'/law/{law}', view_law, name="view_law"),

        web.post('/api/law', api.get.law, name="api_get_law"),
        web.get('/api/law', api.get.law, name="api_get_law"),

        web.post('/api/laws', api.get.laws, name="api_get_laws"),
        web.get('/api/laws', api.get.laws, name="api_get_laws"),

        web.post('/api/law_del', api.post.law_del, name="api_del_law"),
        ])
