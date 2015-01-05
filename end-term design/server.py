#!encoding=utf-8

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os.path

import re
import codecs

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)

name_pattern = re.compile(r"[a-zA-Z0-9]{6,12}")
password_pattern = re.compile(r"[A-Z][a-zA-Z0-9]{5,11}")

def get_Users():
    users_file = open("static/data/userData.txt")
    users_list = users_file.read().strip().split('\n')
    users = []
    for user_item in users_list:
        users.append(user_item.split(','))
    users_file.close()
    return users

def write_Users(users):
    users_file = open("static/data/userData.txt", "w")
    users_list = []
    for user in users:
        users_list.append(','.join(user))
    users_file.writelines('\n'.join(users_list)+'\n')
    users_file.close()

def get_Questions():
    questions_file = open("static/data/questionData.txt")
    questions_list = questions_file.read().strip().split('\n')
    questions = []
    for question_item in questions_list:
        questions.append(question_item.split(';'))
    questions_file.close()
    return questions

def write_Questions(questions):
    questions_file = open("static/data/questionData.txt", "w")
    questions_list = []
    for question in questions:
        questions_list.append(','.join(question))
    questions_file.writelines('\n'.join(questions_list)+'\n')
    questions_file.close()

def get_Replies():
    reply_file = open("static/data/replyData.txt")
    reply_list = reply_file.read()
    if reply_list[:3] == codecs.BOM_UTF8:
        reply_list = reply_list[3:]
    reply_list = reply_list.strip().split('\n')
    reply = []
    for reply_item in reply_list:
        reply.append(reply_item.split(';'))
    reply_file.close()
    return reply


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")


class IndexHandler(BaseHandler):
    def get(self):
        if self.current_user:
            questions = get_Questions()
            replies = get_Replies()
            print replies
            self.render("index.html", questions=questions, replies=replies)
        else:
            self.redirect("/login")
            return
        name = tornado.escape.xhtml_escape(self.current_user)


class QuestionHandler(BaseHandler):
    def get(self):
        if self.current_user:
            new_question = [self.get_argument("title"),
                            self.current_user,
                            self.get_argument("time"),
                            self.get_argument("content"),
                            ]
            questions = get_Questions()
            questions.append(new_question)
            replies = get_Replies()
            print replies
            self.render("index.html", questions=questions, replies=replies)
        else:
            self.redirect("/login")
            return
        name = tornado.escape.xhtml_escape(self.current_user)


class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html", login=2)

    def post(self):
        user = [self.get_argument("name").decode('utf-8'),
                self.get_argument("password").decode('utf-8')]
        users = get_Users()
        if user in users:
            self.set_secure_cookie("user", user[0], expires_days=None)
            self.redirect("/")
        else:
            self.render("login.html", login=False)


class SignUpHandler(BaseHandler):
    def get(self):
        self.render("signup.html", register=2)

    def post(self):
        user = [self.get_argument("name").encode('utf-8'),
                self.get_argument("password").encode('utf-8')]
        users = get_Users()
        print users
        print user
        valid_1 = name_pattern.match(user[0]) and password_pattern.match(user[1])
        valid_2 = not (user[0] == "" or user[1] == "")
        valid_3 = (not user in users)
        print valid_1, valid_2, valid_3
        if valid_1 and valid_2 and valid_3:
            users.append(user)
            write_Users(users)
            self.render("signup.html", register=True)
        else:
            self.render("signup.html", register=False)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/login", LoginHandler),
        (r"/signup", SignUpHandler)],
        template_path=os.path.join(os.path.dirname(__file__), "template"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
        debug=True)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
