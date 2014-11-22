#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael King'

import tornado.web
import json
import tempfile
import Image
import time
import os

import db

#
# 状态信息代码说明

# 100: 成功
# 101: 参数错误
# 102: 该用户已被注册
# 103: 用户名或密码错误
# 104: 结果未找到

class RegisterHandler(tornado.web.RequestHandler):
    def post(self):
        username = self.get_argument('email', '')
        password = self.get_argument('password', '')
        nickname = self.get_argument('nickname', '')
        data = {'status':101}
        if username == '' or password == '' or nickname == '':
            data['status'] = 101
        else :
            sql = "select * from `ofUser` where username=? "
            res = db.select_one(sql, username)  # 查询数据库是否已经被注册过了
            if res is not None :                # 被注册过，status设为失败，并设置已被注册的信息
                data['status'] = 102
            else :                              # 未被注册过，进行注册
                table = "ofUser"
                kw = {"username":username, "password":password, "nickname":nickname}
                res = db.insert(table, **kw)
                data['status']    = 100
        json_result = json.dumps(data , ensure_ascii=False)     # 把python对象编码成json格式的字符串
        self.write(json_result)


class LoginHandler(tornado.web.RequestHandler):
    def post(self):
        username = self.get_argument('email', '')
        password = self.get_argument('password', '')
        data = {'status':103}
        sql = "select * from `ofUser` where username=? and password=? "
        res = db.select_one(sql, username, password)   # 查询数据库，看用户名和密码是否正确
        if res is None :              # 未找到，则用户名或密码不对
            pass
        else :                         # 找到，则用户名密码正确；此时可以确保本次登录成功。
            data['status'] = 100
        json_result = json.dumps(data , ensure_ascii=False)     # 把python对象编码成json格式的字符串
        self.write(json_result)


class EditNicknameHandler(tornado.web.RequestHandler):
    def post(self):
        # 获取post数据
        username = self.get_argument('email', '')
        nickname = self.get_argument('nickname', '')
        # 默认为修改失败
        data = {'status':101, }
        # 构造修改语句
        sql = "update `ofUser` set nickname=? where username=? "  
        # 修改
        res = db.update(sql, nickname, username)
        if res :       # 修改成功
            data['status'] = 100
        else:
            data['status'] = 104
        json_result = json.dumps(data , ensure_ascii=False)     # 把python对象编码成json格式的字符串
        self.write(json_result)


class GetInfoHandler(tornado.web.RequestHandler):
    def post(self):
        username = self.get_argument('email', '')
        data = {'status':101 }
        sql = "select * from `ofUser` where username=? "
        res = db.select_one(sql, username)
        if res :                         # 查找成功
            data['status'] = 100
            info = {}
            info['username'] = username
            if res['nickname']:
                info['nickname'] = res['nickname']#.encode("utf8")
            if res['birthday']:
                info['birthday'] = res['birthday']
            if res['height']:
                info['height']   = res['height']
            if res['weight']:
                info['weight']   = res['weight']
            data['info']     = info
        else:
            data['status'] = 104
        json_result = json.dumps(data, ensure_ascii=False)     # 把python对象编码成json格式的字符串
        self.write(json_result)


class SaveQuestionResultHandler(tornado.web.RequestHandler):
    def post(self):
        username = self.get_argument('email', '')
        birthday = self.get_argument('birthday', '')
        height   = self.get_argument('height', '')
        weight   = self.get_argument('weight', '')

        date     = self.get_argument('date', '')
        result   = self.get_argument('result', '')
        # 默认为修改失败
        data = {'status':101, }
        # 修改用户的最新身高体重
        sql = "update `ofUser` set birthday=?, height=?, weight=? where username=? "
        db.update(sql, birthday, height, weight, username)
        # 问卷结果
        sql = "select * from `ofQuestionResult` where username=? and date=? "
        res = db.select_one(sql, username, date)
        # 今天已经测试过
        if res:
            sql = "update `ofQuestionResult` set birthday=?, height=?, weight=?, result=? where username=? and date=? "
            res = db.update(sql, birthday, height, weight, result, username, date)
        # 今天未测试过
        else:
            table = "ofQuestionResult"
            kw = {"username":username, "birthday":birthday, "height":height, "weight":weight, "date":date, "result":result}
            res = db.insert(table, **kw)
        data['status'] = 100
        json_result = json.dumps(data , ensure_ascii=False)     # 把python对象编码成json格式的字符串
        self.write(json_result)


class GetLastQuestionResultHandler(tornado.web.RequestHandler):
    def post(self):
        username = self.get_argument('email', '')
        data = {'status':101 }
        sql = "select * from `ofQuestionResult` where username=? order by date DESC limit 1"
        res = db.select_one(sql, username)
        if res :                         # 查找成功
            data['status'] = 100
            info = {}
            info['username'] = username
            if res['birthday']:
                info['birthday'] = res['birthday']
            if res['height']:
                info['height']   = res['height']
            if res['weight']:
                info['weight']   = res['weight']
            if res['date']:
                info['date']     = res['date']
            if res['result']:
                info['result']   = res['result']
            data['info']     = info
        else:
            data['status'] = 104
        json_result = json.dumps(data , ensure_ascii=False)     # 把python对象编码成json格式的字符串
        self.write(json_result)


class SaveRecordHandler(tornado.web.RequestHandler):
    def post(self):
        username     = self.get_argument('email', '')
        date         = self.get_argument('date', '')
        heighScore   = self.get_argument('heighScore', '')
        factScore    = self.get_argument('factScore', '')
        exerciseTime = self.get_argument('exerciseTime', '')
        level        = self.get_argument('level', '')
        explosive    = self.get_argument('explosive', '')
        endurance    = self.get_argument('endurance', '')
        exerciseData = self.get_argument('exerciseData', '')
        scoreData    = self.get_argument('scoreData', '')
        # 默认为修改失败
        data = {'status':101, }
        sql = "select * from `ofRecord` where username=? and date=? "
        res = db.select_one(sql, username, date)
        # 已有，则覆盖
        if res:
            sql = "update `ofRecord` set heighScore=?, factScore=?, exerciseTime=?, level=?, explosive=?, endurance=?, exerciseData=?, scoreData=? where username=? and date=? "
            res = db.update(sql, heighScore, factScore, exerciseTime, level, explosive, endurance, exerciseData, scoreData, username, date)
        # 没有，则插入
        else:
            table = "ofRecord"
            kw = {"username":username, "date":date, "heighScore":heighScore, "factScore":factScore, "exerciseTime":exerciseTime, "level":level, "explosive":explosive, "endurance":endurance, "exerciseData":exerciseData, "scoreData":scoreData}
            res = db.insert(table, **kw)
        data['status'] = 100
        json_result = json.dumps(data , ensure_ascii=False)     # 把python对象编码成json格式的字符串
        self.write(json_result)


class GetRecordsHandler(tornado.web.RequestHandler):
    def post(self):
        username = self.get_argument('email', '')
        begin    = self.get_argument('begin', '')
        data = {'status':101 }
            data['records'] = []
        sql = "select * from `ofRecord` where username=? and date >= ?"
        res = db.select(sql, username, begin)
        if res :                         # 查找成功
            data['status'] = 100
            records = [];
            for row in res:
                record = {}
                record['username']     = username
                record['date']         = row['date']
                record['heighScore']   = row['heighScore']
                record['factScore']    = row['factScore']
                record['exerciseTime'] = row['exerciseTime']
                record['level']        = row['level']
                record['explosive']    = row['explosive']
                record['endurance']    = row['endurance']
                record['exerciseData'] = row['exerciseData']
                record['scoreData']    = row['scoreData']
                records.append(record)
            data['records']     = records
        else:
            data['status'] = 104
        json_result = json.dumps(data , ensure_ascii=False)     # 把python对象编码成json格式的字符串
        self.write(json_result)

