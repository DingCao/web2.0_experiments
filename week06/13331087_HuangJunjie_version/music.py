# Copyright (c) 2014 Huang_Junjie@SYSU(SNO:13331087). All Rights Reserved.
''' music.py: LAB3@web2.0_2014_by_PML '''
import os

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)

TITILE = "Music Viewer"
HEADER_1 = "190M Music Playlist Viewer"
HEADER_2 = "Search Through Your Playlists and Music"
MUSIC_LIST = ["Be More.mp3", "Drift Away.mp3", "Hello.mp3", "Panda Sneeze.mp3"]
PLAY_LIST = ["190M Mix.txt", "mypicks.txt", "playlist.txt"]

class IndexHandler(tornado.web.RequestHandler):
    ''' IndexHandler: render the main page '''
    def get(self):
        self.render("music.html", title=TITILE, header1=HEADER_1,
                    header2=HEADER_2, musiclist=MUSIC_LIST, playlist=PLAY_LIST)


class ListHandler(tornado.web.RequestHandler):
    ''' ListHandler: render the pages that we request to only view
        the music list we choose in the playlist '''
    def get(self):
        # get the file name & path
        thislist = "static/songs/"+self.get_argument('playlist', 'NONE')
        thislist.encode("utf-8")
        self.render("list.html", title=TITILE, header1=HEADER_1,
                    header2=HEADER_2,
                    # get the list of files in the list
                    musiclist=open(thislist).readlines(),
                    playlist=[])


if __name__ == "__main__":
    tornado.options.parse_command_line()
    APP = tornado.web.Application(
        handlers=[(r"/", IndexHandler), (r'/list', ListHandler)],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True)  # define this to can exit the python file by keyboard
    HTTP_SERVER = tornado.httpserver.HTTPServer(APP)
    HTTP_SERVER.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
