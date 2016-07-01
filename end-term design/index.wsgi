#-*- encoding:utf-8 -*-

import os.path
import time
import sys
# import _mysql

# personal packages
from handlers import *
from Global import *

settings = {
    "template_path": os.path.join(os.path.dirname(__file__), "template"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/login",
    "debug": True
}

if 'SERVER_SOFTWARE' in os.environ:
    # SAE
    import sae
    import tornado.wsgi
    from sae.ext.storage import monkey
    monkey.patch_all()
    import sae.const

    db_args = (MYSQL_HOST, MYSQL_USER, MYSQL_PASS, MYSQL_DB, int(MYSQL_PORT))

    app = tornado.wsgi.WSGIApplication([
        (r"/", IndexHandler),
        (r"/login", LoginHandler),
        (r"/signup", SignUpHandler),
        (r"/logout", LogoutHandler),
        (r"/question", QuestionHandler),
        (r"/response", ResponseHandler),
        (r".*", WrongHandler)],
        **settings)
    application = sae.create_wsgi_app(app)
else:
    # LOCAL
    import tornado.httpserver
    import tornado.ioloop
    import tornado.options
    import tornado.web
    from tornado.options import define, options
    define("port", default=8888, help="run on the given port", type=int)

    db_args = ('localhost','root','159632', 'scrt_friends', 3306)

    if __name__ == "__main__":
        tornado.options.parse_command_line()
        app = tornado.web.Application([
            (r"/", IndexHandler),
            (r"/login", LoginHandler),
            (r"/signup", SignUpHandler),
            (r"/logout", LogoutHandler),
            (r"/question", QuestionHandler),
            (r"/response", ResponseHandler),
            (r".*", WrongHandler)],
            **settings)
        http_server = tornado.httpserver.HTTPServer(app)
        http_server.listen(options.port)
        tornado.ioloop.IOLoop.instance().start()
