#! encoding=utf-8
# handlers

import re
import os

if 'SERVER_SOFTWARE' in os.environ:
    # SAE
    import sae
    import tornado.wsgi
else:
    import tornado.httpserver
    import tornado.ioloop
    import tornado.options
    import tornado.web

import MySQLdb
import Global

name_pattern = re.compile(r"[a-zA-Z0-9]{6,12}")
password_pattern = re.compile(r"[A-Z][a-zA-Z0-9]{5,11}")

# db operations
def db_connect(db_args):
    return MySQLdb.connect(host=db_args[0], user=db_args[1], \
        passwd=db_args[2], db=db_args[3], port=db_args[4])

#operations on questionsData
def get_Questions():
    # get ten threads
    sql = '''
        SELECT Q.ques_id, Q.ques_name, Q.time, U.uname, Q.ques_context
        FROM Questions Q, users U
        WHERE Q.uid = U.uid
        ORDER BY Q.time DESC
        -- LIMIT 10
    '''
    Global.curs.execute(sql)
    questions = Global.curs.fetchall()
    return questions

def write_Questions(questions):
    questions_file = open("/s/scdata/questionData.txt", "w")
    questions_list = []
    for question in questions:
        questions_list.append(';'.join(question).encode('utf8'))
    questions_file.write('\n'.join(questions_list)+'\n')
    questions_file.close()

#operations on replyData
def get_Replies():
    sql = '''
        SELECT * FROM Replies
        ORDER BY time DESC
    '''
    Global.curs.execute(sql)
    reply = Global.curs.fetchall()
    return reply

def write_Replies(replies):
    reply_file = open("/s/scdata/replyData.txt", "w")
    reply_list = []
    for reply in replies:
        reply_list.append(';'.join(reply).encode('utf-8'))
    reply_file.write('\n'.join(reply_list)+'\n')
    reply_file.close()


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

    def prepare(self):
        Global.db = db_connect(Global.db_args)
        # print Global.db
        Global.curs = Global.db.cursor()

    def on_finish(self):
        Global.db.close()


class IndexHandler(BaseHandler):
    def get(self):
        if self.current_user:
            questions = get_Questions()
            replies = get_Replies()
            # print questions
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
        user = self.get_argument("name").encode('utf-8')
        password = self.get_argument("password").encode('utf-8')

        # qurey from the database
        sql = '''
            SELECT uname, password FROM users
            WHERE uname=(%s) AND password=(%s)
        '''
        Global.curs.execute(sql, (user, password))
        row = Global.curs.fetchone()
        if row:
            self.set_secure_cookie("user", user, expires_days=None)
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
