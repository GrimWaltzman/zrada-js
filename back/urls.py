from views import *
from auth.views import *

def import_urls(app: web.Application):
    app.add_routes([web.get('/', handler_root, name="index"),
        web.get('/login', handler_login, name="login"),
        web.post('/login', handler_login, name="login"),
        web.get('/signin', handler_signin, name="signin"),
        web.post('/signin', handler_signin, name="signin"),
        web.get('/logout', handler_logout, name="logout"),
        web.get('/vote', index, name="vote"),
        web.get('/insert_law', insert_law, name="insert_law"),
        web.post('/insert_law', insert_law, name="insert_law")])
