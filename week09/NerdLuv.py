''' Copyright (c) 2014 Huang_Junjie@SYSU(SNO:13331087). All Rights Reserved. '''
''' NerdLuv.py: Homework4@web2.0_2014_by_PML '''
import os
import re

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)


class Single(object):
    def __init__(self, list_):
        self.name = list_[0]
        self.sex = list_[1]
        self.age = int(list_[2])
        self.personality = list_[3]
        self.OS = list_[4]
        self.seeking = list_[5]
        self.min_age = int(list_[6])
        self.max_age = int(list_[7])

    def match_sex(self, another):
        if self.seeking == u"MF" or another .sex == u"MF":
            return True
        elif self.seeking == another.sex:
            return True
        else:
            return False

    def match_age(self, another):
        if another.age in range(self.min_age, self.max_age+1):
            return True
        else:
            return False

    def match_personality(self, another):
        score = 0
        for i in range(4):
            if self.personality[i] ==another.personality[i]:
                score += 1

        return score

    def get_Matches(self, singles):
        matches = []
        for single in singles:
            if self.match_sex(single) and single.match_sex(self):
                point = 0
                if self.match_age(single) and single.match_age(self):
                    point +=1
                if self.OS == single.OS:
                    point += 2

                point += self.match_personality(single)
                if point >= 3:
                    single.point = point
                    single.image_name = '_'.join(single.name.lower().split())
                    matches.append(single)
            else:
                continue

        return matches



class IndexHandler(tornado.web.RequestHandler):
    ''' IndexHandler: render the index page '''
    def get(self):
        self.render("index.html")


class ResultHandler(tornado.web.RequestHandler):
    ''' IndexHandler: render the index page '''
    def get_User_List(self, name, sex, age,
                      personality, OS, seeking,
                      min_age, max_age):
        a_list = []
        a_list.append(name)
        a_list.append(sex)
        a_list.append(int(age))
        a_list.append(personality)
        a_list.append(OS)

        a_list.append("")
        for seek in seeking:
            a_list[5] += seek

        a_list.append(int(min_age))
        a_list.append(int(max_age))

        return a_list

    def get_Singles(self):
        singles_file = open("statics/singles.txt")
        singlers_lines = singles_file.read().strip().split('\n')
        singles_file.close()

        singlers = []
        for line in  singlers_lines:
            single = Single(line.split(','))
            singlers.append(single)

        return singlers

    def write_Singles(self, singles):
        list_ = []
        for single in singles:
            item = [single.name, single.sex, str(single.age),
                    single.personality, single.OS, single.seeking,
                    str(single.min_age), str(single.max_age)]
            item = ','.join(item)
            item.decode('utf-8')
            list_.append(item)

        print list_
        singles_file = open("statics/singles.txt", "w")
        singles_file.writelines('\n'.join(list_))

    def post(self):
        user_list = self.get_User_List(self.get_argument('name'),
                                       self.get_argument('gender'),
                                       self.get_argument('age'),
                                       self.get_argument('personality'),
                                       self.get_argument('os'),
                                       self.get_arguments('seeking'),
                                       self.get_argument('min-age'),
                                       self.get_argument('max-age'))
        user = Single(user_list)

        singles = self.get_Singles()
        if not user in singles:
            singles.append(user)

        matches = user.get_Matches(singles)

        self.write_Singles(singles)
        self.render("results.html", user_name=user.name, matches=matches)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    APP = tornado.web.Application(
        handlers=[(r'/index', IndexHandler), (r'/result', ResultHandler)],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "statics"),
        debug=True)  # define this to can exit the python file by keyboard
    HTTP_SERVER = tornado.httpserver.HTTPServer(APP)
    HTTP_SERVER.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
