#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael King'

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import json
import time
import os


from tornado.options import define, options

define("port", default=8001, help="upload test file", type=int)

settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "upload"),
    }


class UploadHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("it works!")

    def post(self):
        imei = self.get_argument('imei', 'unkonwn')
        # 默认为修改失败
        data = {'status':False, 'msg':'上传失败'}
        file_meta = self.request.files['file'][0]    # 提取表单中 'name' 为'file'的文件元数据(只得到文件列表中的第一个)
        filename = file_meta['filename'] # str(int(time.time())) + '.txt'   # 后缀：file_meta['filename'].split('.').pop().lower()

        file_path = os.path.join(os.path.dirname(__file__), "upload", imei)
        # 如果文件夹不存在，则创建文件夹
        if not os.path.isdir(file_path):
            os.makedirs(file_path)
        full_name = os.path.join(file_path, filename)
        with open(full_name, 'wb') as up: # 某些文件是二进制的
            up.write(file_meta['body'])
            data['status'] = True
            data['msg']    = '上传成功'
        # 用户上传图片成功 判断结束
        json_result = json.dumps(data , ensure_ascii=False)     # 把python对象编码成json格式的字符串
        self.write(json_result)

application = tornado.web.Application([
    (r"/",   UploadHandler),
], **settings)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


