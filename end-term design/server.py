#-*- encoding:utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os
import re
import time
import sys

reload(sys)  
sys.setdefaultencoding('utf8')

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("username")

class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        myfile = open('static/data/questionData.txt', 'a+')
        lists = myfile.readlines()
        lists1 = []
        for item in lists:
            lists1.append(re.split(';', item.replace('\n', '')))
        myfile.close()
        myfile = open('static/data/replyData.txt', 'a+')
        lists = myfile.readlines()
        for it in lists1:
            lists2 = []
            for item in lists:
                info = re.split(';', item.replace('\n', ''))
                if info[0] == it[2]:
                    lists2.append(info)
            it.append(lists2)
        myfile.close()
        self.render("index.html",
            title = "主页",
            list1 = lists1
        )

class SignupHandler(BaseHandler):
    def get(self):
        if self.current_user:
            self.redirect('/')
        else:
            self.render('login_signup.html',
                title = "注册页面",
                button = "注册",
                link1 = "已有账号？点击登录",
                url = "/login",
                action = "/signup"
            )
    def post(self):
        name = self.get_argument("name", None)
        password = self.get_argument("password", None)
        if not re.match('([0-9]|[A-Z]|[a-z]){6,12}$', name) or \
            not re.match('[A-Z]{1}([0-9]|[a-z]|[A-Z]){5,11}$', password):
            return self.render('login_signup.html',
                title = "注册页面",
                button = "注册",
                link1 = "已有账号？点击登录",
                url = "/login",
                action = "/signup"
            )
        if name and password:
            myfile = open('static/data/userData.txt', 'a+')
            lists = myfile.readlines()
            for item in lists:
                for x in xrange(0, len(item)):
                    if item[x] == ',':
                        listname = item[:x]
                        if listname == name:
                            return self.render('login_signup.html',
                                title = "注册页面",
                                button = "注册",
                                link1 = "已有账号？点击登录",
                                url = "/login",
                                action = "/signup"
                            )
            myfile.write(name + ',' + password + '\n')
            myfile.close()
            self.set_secure_cookie("username", name)
            return self.redirect("/")
        return self.render('login_signup.html',
            title = "注册页面",
            button = "注册",
            link1 = "已有账号？点击登录",
            url = "/login",
            action = "/signup"
        )

class LoginHandler(BaseHandler):
    def get(self):
        if self.current_user:
            self.redirect('/')
        else:
            self.render('login_signup.html',
                title = "登录页面",
                button = "登录",
                link1 = "没有账号？点击注册",
                url = "/signup",
                action = "/login"
            )
    def post(self):
        name = self.get_argument("name", None)
        password = self.get_argument("password", None)
        if name and password:
            myfile = open('static/data/userData.txt', 'a+')
            lists = myfile.readlines()
            for item in lists:
                for x in xrange(0, len(item)):
                    if item[x] == ',':
                        listname = item[:x]
                        listpassword = item[x + 1:-2]
                        print listname,listpassword
                        if listname == name and password == listpassword:
                            myfile.close()
                            self.set_secure_cookie("username", name)
                            return self.redirect("/")
            myfile.close()
            return self.render('login_signup.html',
                title = "登录页面",
                button = "登录",
                url = "/signup",
                link1 = "没有账号？点击注册",
                action = "/login"
            )
        return self.render('login_signup.html',
            title = "登录页面",
            button = "登录",
            link1 = "没有账号？点击注册",
            url = "/signup",
            action = "/login"
        )

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("username")
        return self.redirect("/login")

class QuestionHandler(BaseHandler):
    def get(self):
        if self.current_user:
            self.render('question.html',
                title = "提问页面",
                subtitle = "问题",
                uptime = "提交时间",
                uptext = "问题内容",
                button = "提交问题"
            )
        else:
            self.render('login_signup.html',
                title = "登录页面",
                button = "登录",
                link1 = "没有账号？点击注册",
                url = "/signup",
                action = "/login"
            )
    def post(self):
        stitle = self.get_argument('title', None)
        stime = self.get_argument('time', None)
        stext = self.get_argument('content', None)
        if re.search(';', stitle) or re.search(';', stitle) or \
            re.search(';', stitle):
            return self.render('question.html',
                title = "提问页面",
                subtitle = "问题",
                uptime = "提交时间",
                uptext = "问题内容",
                button = "提交问题"
            )
        if stitle and stime and stext:
            myfile = open('static/data/questionData.txt', 'a+')
            myfile.write(stitle + ';' + stime + ';' + \
                self.current_user + ';' + stext + '\n')
            myfile.close()
            return self.redirect('/')
        return self.render('question.html',
            title = "提问页面",
            subtitle = "问题",
            uptime = "提交时间",
            uptext = "问题内容",
            button = "提交问题"
        )

class WrongHandler(tornado.web.RequestHandler):
    def get(self):
        self.write_error(404)
    
    def write_error(self, status_code, **kwages):
        if status_code == 404:
            self.render('404.html', title = "404")
        else:
            self.write('Ah ha! error:' + str(status_code))

class ResponseHandler(BaseHandler):
    def post(self):
        responsetext = self.get_argument('responsetext', None)
        responseauthor = self.get_argument('author', None)
        if responsetext and responseauthor:
            myfile = open('static/data/replyData.txt', 'a+')
            myfile.write(responseauthor + ';' + \
                time.strftime("%Y-%m-%d %H:%M") + ';' + \
                self.current_user + ';' + responsetext + '\n')
            myfile.close()
        return self.redirect('/')

if __name__ == "__main__":
    tornado.options.parse_command_line()
    settings = {
        "template_path": os.path.join(os.path.dirname(__file__), "template"),
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "cookie_secret": "bZdJc2sWbegffdd/QLeKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
        "login_url": "/login"
    }
    app = tornado.web.Application(handlers=[
        (r"/", IndexHandler),
        (r"/signup", SignupHandler),
        (r"/login", LoginHandler),
        (r"/logout", LogoutHandler),
        (r"/question", QuestionHandler),
        (r"/response", ResponseHandler),
        (r".*", WrongHandler)
    ], **settings)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
