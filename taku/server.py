#!/usr/bin/env python
# -*- coding: utf-8 -*-

#                       _ooOoo_ 
#                      o8888888o 
#                      88" . "88 
#                      (| -_- |) 
#                      O\  =  /O 
#                   ____/`---'\____ 
#                 .'  \\|     |//  `. 
#                /  \\|||  :  |||//  \ 
#               /  _||||| -:- |||||-  \ 
#               |   | \\\  -  /// |   | 
#               | \_|  ''\---/''  |   | 
#               \  .-\__  `-`  ___/-. / 
#             ___`. .'  /--.--\  `. . __ 
#          ."" '<  `.___\_<|>_/___.'  >'"". 
#         | | :  `- \`.;`\ _ /`;.`/ - ` : | | 
#         \  \ `-.   \_ __\ /__ _/   .-` /  / 
#    ======`-.____`-.___\_____/___.-`____.-'====== 
#                       `=---=' 
#    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 
#                  佛祖镇楼                  BUG辟易
#        佛曰:
#                  写字楼里写字间，写字间里程序员；
#                  程序人员写程序，又拿程序换酒钱。
#                  酒醒只在网上坐，酒醉还来网下眠；
#                  酒醉酒醒日复日，网上网下年复年。
#                  但愿老死电脑间，不愿鞠躬老板前；
#                  奔驰宝马贵者趣，公交自行程序员。
#                  别人笑我忒疯癫，我笑自己命太贱；
#                  不见满街漂亮妹，哪个归得程序员？

__author__ = 'Michael King'

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from handler import *

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "cookie_secret": "MtaYBHulSEa1nOyCKH9oM4fooUMSo0ewqIMTMVbMWxA=",
    }

application = tornado.web.Application([
    (r"/register",     RegisterHandler),
    (r"/login",        LoginHandler),
    (r"/logout",       LogoutHandler),
    (r"/editinfo",     EditInfoHandler),
    (r"/getinfo",      GetInfoHandler),
    (r"/changeavatar", ChageAvatarHandler),
    (r"/getavatar",    GetAvatarHandler),
], **settings)



if __name__ == "__main__":
    db.create_engine('root', 'Linkcube2013', 'taku')
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


