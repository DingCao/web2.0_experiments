#! encoding=utf-8

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os.path

import re
import time


from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)

name_pattern = re.compile(r"[a-zA-Z0-9]{6,12}")
password_pattern = re.compile(r"[A-Z][a-zA-Z0-9]{5,11}")

#file input-output functions
#operations on userData
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
    users_file.write('\n'.join(users_list)+'\n')
    users_file.close()

#operations on questionsData
def get_Questions():
    questions_file = open("static/data/questionData.txt")
    questions_list = questions_file.read().decode('utf8').strip().split('\n')
    questions = []
    for question_item in questions_list:
        questions.append(question_item.split(';'))
    questions_file.close()
    return questions

def write_Questions(questions):
    questions_file = open("static/data/questionData.txt", "w")
    questions_list = []
    for question in questions:
        questions_list.append(';'.join(question).encode('utf8'))
    questions_file.write('\n'.join(questions_list)+'\n')
    questions_file.close()

#operations on replyData
def get_Replies():
    reply_file = open("static/data/replyData.txt")
    reply_list = reply_file.read().decode('utf8').strip().split('\n')
    reply = []
    for reply_item in reply_list:
        reply.append(reply_item.split(';'))
    reply_file.close()
    return reply

def write_Replies(replies):
    reply_file = open("static/data/replyData.txt", "w")
    reply_list = []
    for reply in replies:
        reply_list.append(';'.join(reply).encode('utf-8'))
    reply_file.write('\n'.join(reply_list)+'\n')
    reply_file.close()


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")


class IndexHandler(BaseHandler):
    def get(self):
        if self.current_user:
            questions = get_Questions()
            questions = questions[::-1]
            replies = get_Replies()
            self.render("index.html",title='主页', Username=self.current_user,
                        questions=questions, replies=replies)
        else:
            self.redirect("/login")
            return
        name = tornado.escape.xhtml_escape(self.current_user)


class LoginHandler(BaseHandler):
    def get(self):
        self.render("login_signup.html", title="登录页面", button="登录",
                    link="没有账号？点击注册", url="/signup", action="/login",
                    subtitle="")

    def post(self):
        user = [self.get_argument("name").encode('utf-8'),
                self.get_argument("password").encode('utf-8')]
        users = get_Users()
        if user in users:
            self.set_secure_cookie("user", user[0], expires_days=None)
            self.redirect("/")
        else:
            self.render("login_signup.html", title="登录页面", button="登录",
                        link="没有账号？点击注册", url="/signup",
                        action="/login", subtitle="登录失败，请重新尝试")


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_all_cookies()
        return self.redirect("/login")


class SignUpHandler(BaseHandler):
    def get(self):
        self.render("login_signup.html", title = "注册页面", button="注册",
                    link="已有账号？点击登录",
                    url="/login", action="/signup", subtitle="")

    def post(self):
        user = [self.get_argument("name").encode('utf-8'),
                self.get_argument("password").encode('utf-8')]
        users = get_Users()

        valid_1 = name_pattern.match(user[0]) and \
                  password_pattern.match(user[1])

        # avoid the same user be registered again by other password
        valid_2 = True
        for user_item in users:
            if user_item[0] == user[0]:
                valid_2 = False

        if valid_1 and valid_2:
            users.append(user)
            write_Users(users)
            self.render("login_signup.html", title = "注册页面", button="注册",
                        link="已有账号？点击登录",
                        url="/login", action="/signup",
                        subtitle="注册成功！请前往登录页面登录")
        else:
            self.render("login_signup.html", title = "注册页面", button="注册",
                        link="已有账号？点击登录",
                        url="/login", action="/signup",
                        subtitle="注册失败，请重新尝试")


# coded by YaoShaoling, correted by HuangJunjie
class QuestionHandler(BaseHandler):
    def get(self):
        if self.current_user:
            self.render('question.html', title="提问页面", subtitle="问题",
                        uptext="问题内容", button="提交问题",
                        Username=self.current_user)
        else:
            self.redirect("/login")

    def post(self):
        questions = get_Questions()
        stitle = self.get_argument('title', None)
        stime = time.strftime("%Y-%m-%d %H:%M")
        stext = self.get_argument('content', None)
        invalid_1 = re.search(';', stitle) or re.search(';', stext)
        invalid_2 = re.search('\n', stitle)or re.search('\n', stext)
        if invalid_1 or invalid_2:
            return self.render('question.html', title="提问页面",
                               subtitle="问题",
                               uptext="问题内容", button="提交问题",
                               Username=self.current_user)

        if stitle and stime and stext:
            new_question = [stitle, stime, self.current_user, stext]
            questions.append(new_question)
            write_Questions(questions)
            return self.redirect('/')

        return self.render('question.html', title="提问页面", subtitle="问题",
                            uptext="问题内容",
                            button="提交问题", Username=self.current_user)


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
        replies = get_Replies()
        responsetext = self.get_argument('responsetext', None)
        responsetitle = self.get_argument('title', None)
        if responsetext and responsetitle:
            new_reply = [responsetitle, time.strftime("%Y-%m-%d %H:%M"),
                         self.current_user, responsetext]
            replies.append(new_reply)
            write_Replies(replies)
        return self.redirect('/')


settings = {
    "template_path": os.path.join(os.path.dirname(__file__), "template"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/login",
    "debug": True
}

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
        **settings
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
