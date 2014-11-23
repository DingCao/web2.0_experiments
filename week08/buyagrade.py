''' Copyright (c) 2014 Huang_Junjie@SYSU(SNO:13331087). All Rights Reserved.
    buyagrade.py: LAB4@web2.0_2014_by_PML '''
import os
import re

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)


OPTIONS_FILE = open("statics/data/options.txt")
OPTIONS = OPTIONS_FILE.read().split('\n')
OPTIONS_FILE.close()

def find(name, NAMES):
    for this_name in NAMES:
        if this_name == name:
            return True
    return False

def cardConvert(card_number):
    ''' if a card_number is valid, throw the '-' character in it '''
    return ''.join(card_number.split('-'))

def isCardValid(card_number, card_type):
    ''' |pattern| to match the card_number if the card_number is valid '''
    pattern = re.compile(r'([45]\d{3})(\-?)\d{4}\2\d{4}\2\d{4}')
    return pattern.match(card_number) and \
        ((card_number.startswith("4") and card_type == "visa") or \
        (card_number.startswith("5") and card_type == "mastercard"))

def Luhn(card_number):
    ''' whether the card_number is wrong '''
    sum = 0
    nums = card_number[::-1].decode("utf-8")
    temp = 0

    for i in range(len(card_number)):
        if i%2:
            temp = int(nums[i])
        else:
            temp = int(nums[i]) * 2
            if temp > 9:
                temp = temp/10 + temp%10
        sum += temp

    return sum%10


class MainHandler(tornado.web.RequestHandler):
    ''' MainHandler: render the main pages '''
    def get(self):
        self.render("buyagrade.html", options=OPTIONS)


class SuckerHandler(tornado.web.RequestHandler):
    ''' SuckerHandler: render the sucker.html.
        if the form is unvalid, render the sucker page with error message. '''

    def post(self):
        # first gets the arguments
        name = self.get_argument('name')
        section = self.get_argument('section')
        card_number = self.get_argument('card-number')
        card_type = self.get_argument('card-type', 'none')

        # determines if all the message is filled
        is_valid1 = (name != "") and find(section, OPTIONS) \
                    and (card_number != "") and (card_type != 'none')

        # determines whether the card message is valid
        if (isCardValid(card_number, card_type)):
            card_number = cardConvert(card_number)
            if not Luhn(card_number):
                is_card_valid = True
            else:
                is_card_valid = False
        else:
            is_card_valid = False

        # determines what pages we should respones
        if is_valid1 and is_card_valid:
            suckers_file = open("statics/data/suckers.txt")
            suckers = suckers_file.readlines()
            suckers_file.close()

            this_sucker = name+';'+section+';'+card_number+';'+card_type
            if not this_sucker+'\n' in suckers:
                suckers.append(this_sucker+'\n')

                suckers_file = open("statics/data/suckers.txt", "w")
                suckers_file.writelines(suckers)
                suckers_file.close()

            suckers_file = open("statics/data/suckers.txt")
            self.render('sucker.html', name=name, section=section,
                    card_number=card_number, card_type=card_type,
                    suckers=suckers_file.read())
            suckers_file.close()

        elif is_valid1 and (not is_card_valid):
            self.render("error.html", error_message="You din;'t provide a \
                        valid card number.")

        else:
            self.render("error.html", error_message="You din;'t fill out the \
                        form completely.")


if __name__ == "__main__":
    tornado.options.parse_command_line()
    APP = tornado.web.Application(
        handlers=[(r'/buyagrade.py', MainHandler),
        (r'/buyagrade.py/sucker.html', SuckerHandler)],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "statics"),
        debug=True)  # define this to can exit the python file by keyboard
    HTTP_SERVER = tornado.httpserver.HTTPServer(APP)
    HTTP_SERVER.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
