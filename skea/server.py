#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael King'

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from handler import *

from tornado.options import define, options
define("port", default=8002, help="run on the given port", type=int)

settings = {
#        "static_path": os.path.join(os.path.dirname(__file__), "static"),
    }

application = tornado.web.Application([
    (r"/register",              RegisterHandler),
    (r"/login",                 LoginHandler),
    (r"/editNickname",          EditNicknameHandler),
    (r"/getInfo",               GetInfoHandler),
    (r"/saveQuestionResult",    SaveQuestionResultHandler),
    (r"/getLastQuestionResult", GetLastQuestionResultHandler),
    (r"/saveRecord",            SaveRecordHandler),
    (r"/getRecords",            GetRecordsHandler),
    (r"/findPassword",          FindPasswordHandler),

], **settings)



if __name__ == "__main__":
    # db.create_engine('root', 'root', 'skea')  # 本地测试使用
    db.create_engine('root', 'Linkcube2013', 'skea')
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


