# Copyright (c) 2014 Huang_Junjie@SYSU(SNO:13331087). All Rights Reserved.
''' : LAB3@web2.0_2014_by_PML '''
import os

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)


class FilmHandler(tornado.web.RequestHandler):
    ''' ListHandler: render the pages that we request to only view
        the music list we choose in the playlist '''
    def get(self):
        # get the file name & path
        path = "static/"+self.get_argument('movie')+"/"
        path.encode("utf-8")

        info = open(path+"info.txt").readlines()
        generaloverview = open(path+"generaloverview.txt").readlines()
        general = []
        for overview in generaloverview:
            general.append(overview.split(':'))

        commentslist = []
        files = os.listdir(path)
        for a_file in files:
            if a_file.startswith("review"):
                commentslist.append(a_file)

        commentlist1 = []
        commentlist2 = []
        for i in range(len(commentslist)):
            temp_comment = open(path+commentslist[i]).readlines()
            if i%2 :
                commentlist2.append(temp_comment)
            else :
                commentlist1.append(temp_comment)

        self.render("movie.html",
                    title=info[0], year=info[1],
                    percent=info[2], total=info[3],
                    generaloverview=general,
                    commentlist1=commentlist1, commentlist2=commentlist2)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    APP = tornado.web.Application(
        handlers=[(r'/', FilmHandler)],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True)  # define this to can exit the python file by keyboard
    HTTP_SERVER = tornado.httpserver.HTTPServer(APP)
    HTTP_SERVER.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
