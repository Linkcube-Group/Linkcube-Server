#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael King'

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from handler import *

from tornado.options import define, options
define("port", default=8001, help="run on the given port", type=int)

#settings = {
#        "static_path": os.path.join(os.path.dirname(__file__), "static"),
#    }

application = tornado.web.Application([
    (r"/register",             RegisterHandler),
    (r"/login",                LoginHandler),
    (r"/logout",               LogoutHandler),
    (r"/editNickname",         EditNicknameHandler),
    (r"/getInfo",              GetInfoHandler),
#    (r"/changeavatar",         ChageAvatarHandler),
#    (r"/getavatar",            GetAvatarHandler),
#    (r"/uploadGameRecord",     UploadRecordHandler),
#    (r"/getSingleDayHistory",  SingleDayRecordHandler),
#    (r"/getTotalHistory",      TotalRecordHandler),

], **settings)



if __name__ == "__main__":
    # db.create_engine('root', 'root', 'taku')  # 本地测试使用
    db.create_engine('root', 'root', 'skea')
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


