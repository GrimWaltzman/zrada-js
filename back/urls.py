from views import *
from auth.views import *

def import_urls(app: web.Application):
    app.add_routes([web.get('/', handler_root, name="index"),
        web.get('/login', handler_login, name="login"),
        web.post('/login', handler_login, name="login"),
        web.get('/signin', handler_signin, name="signin"),
        web.get('/logout', handler_logout, name="logout"),
        web.get('/listen', handler_listen, name="listen"),
        web.get('/speak', handler_speak, name="speak"),
        web.get('/vote', index, name="vote")])
