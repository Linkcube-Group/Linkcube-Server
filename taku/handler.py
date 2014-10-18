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

import tornado.web
import json
import tempfile
import Image
import time
import os

import db

class RegisterHandler(tornado.web.RequestHandler):
    def post(self):
        username = self.get_argument('email')
        password = self.get_argument('pwd')
        data = {'status':False, 'msg':''}
        if username == '' or password == '':
            data['msg'] = '用户名和密码均不能为空'
        else :
            sql = "select * from `ofUser` where username=? "
            res = db.select_one(sql, username)  # 查询数据库是否已经被注册过了
            if res is not None :                # 被注册过，status设为失败，并设置已被注册的信息
                data['msg'] = '该邮箱已被注册'
            else :                              # 未被注册过，进行注册
                table = "ofUser"
                kw = {"username":username, "password":password}
                res = db.insert(table, **kw)
                data['status'] = True
                data['msg']    = '注册成功'
        json_result = json.dumps(data , ensure_ascii=False)     # 把python对象编码成json格式的字符串
        self.write(json_result)


class LoginHandler(tornado.web.RequestHandler):
    def post(self):
        username = self.get_argument('email')
        password = self.get_argument('pwd')
        data = {'status':False}

        sql = "select * from `ofUser` where username=? and password=? "
        res = db.select_one(sql, username, password)   # 查询数据库，看用户名和密码是否正确
        if res is None :              # 未找到，则用户名或密码不对
            pass
        else :                         # 找到，则用户名密码正确；此时可以确保本次登录成功。
            data['status'] = True
            self.set_secure_cookie("username", username)
        json_result = json.dumps(data , ensure_ascii=False)     # 把python对象编码成json格式的字符串
        self.write(json_result)

class LogoutHandler(tornado.web.RequestHandler):
    def post(self):
        username = self.get_secure_cookie("username")
        data = {'status':True, 'msg':'注销成功'}
        self.clear_cookie("username")
        json_result = json.dumps(data , ensure_ascii=False)     # 把python对象编码成json格式的字符串
        self.write(json_result)

class EditInfoHandler(tornado.web.RequestHandler):
    def post(self):
        # 获取cookie保证用户已登录
        username = self.get_secure_cookie("username")
        # 获取post数据
        nickname = self.get_argument('nickname', '')
        gender   = self.get_argument('gender', '男')
        age      = self.get_argument('age', '18')
        height   = self.get_argument('height', '')
        weight   = self.get_argument('weight', '')
        # 默认为修改失败
        data = {'status':False, 'msg':'修改失败'}
        # 构造修改语句
        sql = "update `ofUser` set nickname=?, gender=?, age=?, height=?, weight=? where username=? "  
        # 修改
        res = db.update(sql, nickname, gender, int(age), height, weight, username)
        if res :       # 修改成功
            data['status'] = True
            data['msg']    = '修改成功'
        json_result = json.dumps(data , ensure_ascii=False)     # 把python对象编码成json格式的字符串
        self.write(json_result)


class GetInfoHandler(tornado.web.RequestHandler):
    def post(self):
        username = self.get_secure_cookie("username")
        data = {'status':False, 'msg':'获取失败'}
        sql = "select * from `ofUser` where username=? "
        res = db.select_one(sql, username)
        if res :                         # 查找成功
            data['status'] = True
            data['msg']    = '获取成功'
            info = {}
            info['username'] = username
            if res['nickname']:
                info['nickname'] = res['nickname'].encode("utf8")
            else :
                info['nickname'] = res['nickname']
            if res['gender']:
                info['gender']   = res['gender'].encode("utf8")
            else :
                info['gender']   = res['gender']
            # age为int，不需要编码
            info['age']      = res['age']
            if res['height']:
                info['height']   = res['height'].encode("utf8")
            else :
                info['height']   = res['height']
            if res['weight']:
                info['weight']   = res['weight'].encode("utf8")
            else :
                info['weight']   = res['weight']
            if res['avatar']:
                info['avatar']   = res['avatar'].encode("utf8")
            else :
                info['avatar']   = res['avatar']
            data['info']     = info
        json_result = json.dumps(data , ensure_ascii=False)     # 把python对象编码成json格式的字符串
        self.write(json_result)

class ChageAvatarHandler(tornado.web.RequestHandler):
    def post(self):
        # 获取cookie保证用户已登录
        username = self.get_secure_cookie("username")
        # 默认为修改失败
        data = {'status':False, 'msg':'修改失败'}
        # request.files会有这种格式的信息:{"avatar":[{'filename':'', 'content_type':'', 'body':''}]}
        # filename为客户端的文件名字; content_type为MIME类型，如image/gif, image/jpeg, image/png等; body为文件内容
        if self.request.files == {} or 'avatar' not in self.request.files: # 没有所需上传文件
            data['msg']    = '上传文件失败'
        else :
            # 常用的图片格式有：image/jpeg，image/bmp，image/pjpeg，image/gif，image/x-png，image/png
            image_type_list = ['image/gif', 'image/jpeg', 'image/pjpeg', 'image/bmp', 'image/png', 'image/x-png']
            # 得到文件对象
            send_file = self.request.files['avatar'][0]
            # 限制文件格式
            if send_file['content_type'] not in image_type_list:
                data['msg'] = '请上传jpeg、gif、png、bmp等常见格式的图片'
            # 限制文件大小
            elif len(send_file['body']) > 4 * 1024 * 1024:
                data['msg'] = '请上传4M以下的图片'
            # 满足所有要求,存储图片
            else:
                # 存储也就是将send_file['body']内容进行存储，type(send_file['body'])为str
                # 先将文件写入临时文件，然后再用PIL对这个临时文件进行处理。
                tmp_file = tempfile.NamedTemporaryFile(delete=True) #创建临时文件，当文件关闭时自动删除
                tmp_file.write(send_file['body'])  #写入临时文件
                tmp_file.seek(0)   #将文件指针指向文件头部，因为上面的操作将指针指向了尾部
                #此时用PIL再处理进行存储，PIL打开不是图片的文件会出现IOERROR错误，这就可以识别后缀名虽然是图片格式，但内容并非是图片。
                try:
                    image_one = Image.open( tmp_file.name )
                except IOError, error:
                    tmp_file.close()
                    data['msg'] = '图片格式不合法'
                    # 出错直接返回
                    json_result = json.dumps(data , ensure_ascii=False)     # 把python对象编码成json格式的字符串
                    self.write(json_result)
                    return
                # 判断图片尺寸，不在尺寸内拒绝操作
                #if image_one.size[0] < 250 or image_one.size[1] < 250 or image_one.size[0] > 2000 or image_one.size[1] > 2000:
                #    tmp_file.close()
                #    data['msg'] = '图片长宽必须在250px~2000px之间'
                    # 尺寸不对直接返回
                #    json_result = json.dumps(data , ensure_ascii=False)     # 把python对象编码成json格式的字符串
                #    self.write(json_result)
                #    return
                # 进行存储
                # 指定存储目录，产生新的文件名
                # 获取文件格式，用PIL获得的format不一定正确，所以用原文件名获得
                image_path = "static/"                                     # 指定文件存储路径
                image_format = send_file['filename'].split('.').pop().lower() # 得到后缀
                tmp_name = image_path + str(int(time.time())) + '.' + image_format  # 文件名
                image_one.save(tmp_name)
                #关闭临时文件，关闭后临时文件自动删除
                tmp_file.close()

                # 先从数据库中取出旧文件地址，删除旧文件
                sql = "select avatar from `ofUser` where username=? "
                res = db.select_one(sql, username)
                if res and res['avatar']:
                    old_file = res['avatar'].encode("utf8")
                    if os.path.isfile(old_file):  # 删除旧文件
                        os.remove(old_file)

                # 将新文件地址存入数据库
                sql = "update `ofUser` set avatar=? where username=? "  
                # 修改
                res = db.update(sql, tmp_name, username)
                if res :       # 修改成功
                    data['status'] = True
                    data['msg']    = '修改成功'
            # 满足要求的图片 判断结束
        # 用户上传图片成功 判断结束
        json_result = json.dumps(data , ensure_ascii=False)     # 把python对象编码成json格式的字符串
        self.write(json_result)

class GetAvatarHandler(tornado.web.RequestHandler):
    def post(self):
        # 获取cookie保证用户已登录
        username = self.get_secure_cookie("username")
        # 默认为修改失败
        data = {'status':False, 'msg':'获取失败'}
        # 从数据库中取出头像地址
        sql = "select avatar from `ofUser` where username=? "
        res = db.select_one(sql, username)
        if res and res['avatar']:
            avatar = res['avatar'].encode("utf8")
            data['avatar'] = avatar
            data['status'] = True
            data['msg']    = '获取成功'
        json_result = json.dumps(data , ensure_ascii=False)     # 把python对象编码成json格式的字符串
        self.write(json_result)


class UploadRecordHandler(tornado.web.RequestHandler):
    def post(self):
        # 获取cookie保证用户已登录
        username = self.get_secure_cookie("username")
        # 获取post数据
        recordDate = self.get_argument('recordDate', '')
        duration   = int(self.get_argument('duration', '0'))
        distance   = int(self.get_argument('distance', '0'))
        calorie    = int(self.get_argument('calorie', '0'))
        data = {'status':False, 'msg':''}
        sql = "select id from `ofRecord` where username=? and recordDate=?"
        res = db.select_one(sql, username, recordDate)
        if res is not None :                # 已上传过，更新信息
            recordID = res['id']
            sql = "update `ofRecord` set recordDate=?, duration=?, distance=?, calorie=? where id=? "
            res = db.update(sql, recordDate, duration, distance, calorie, recordID)
        else :                              # 未上传过，插入信息
            table = "ofRecord"
            kw = {"username":username, "recordDate":recordDate, "duration":duration, "distance":distance, "calorie":calorie}
            res = db.insert(table, **kw)
        if res :       # 修改成功
            data['status'] = True
            data['msg']    = '修改成功'
        json_result = json.dumps(data , ensure_ascii=False)     # 把python对象编码成json格式的字符串
        self.write(json_result)


class SingleDayRecordHandler(tornado.web.RequestHandler):
    def post(self):
        username = self.get_secure_cookie("username")
        # 获取post数据
        recordDate = self.get_argument('historyDate', '')
        data = {'status':False, 'msg':'该日期无记录'}
        sql = "select * from `ofRecord` where username=? and recordDate=? "
        res = db.select_one(sql, username, recordDate)
        if res :                         # 查找成功
            data['status'] = True
            data['msg']    = '获取成功'
            info = {}
            info['username'] = username
            # int值不需要编码
            info['singleDayDuration']      = res['duration']
            info['singleDayDistance']      = res['distance']
            info['singleDayCalorie']       = res['calorie']
            data['info']     = info
        json_result = json.dumps(data , ensure_ascii=False)     # 把python对象编码成json格式的字符串
        self.write(json_result)


class TotalRecordHandler(tornado.web.RequestHandler):
    def post(self):
        username = self.get_secure_cookie("username")
        data = {'status':False, 'msg':'无记录'}
        sql = "select sum(duration), sum(distance), sum(calorie) from `ofRecord` where username=? "
        res = db.select_one(sql, username)
        if res :                         # 查找成功
            data['status'] = True
            data['msg']    = '获取成功'
            info = {}
            info['username'] = username
            # int值不需要编码
            info['TotalDuration']      = int(res['sum(calorie)'])
            info['TotalDistance']      = int(res['sum(distance)'])
            info['TotalCalorie']       = int(res['sum(duration)'])
            data['info']     = info
        json_result = json.dumps(data , ensure_ascii=False)     # 把python对象编码成json格式的字符串
        self.write(json_result)
