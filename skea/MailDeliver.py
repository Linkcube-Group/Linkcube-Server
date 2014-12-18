#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael King'

import smtplib  
from email.mime.text import MIMEText  
from email.header import Header  
  
# 对外函数
def sendPassword(email, password):
    # 参数配置
    smtpserver = 'smtp.163.com'
    sender   = 'linkcube2013@163.com'  
    senderUsername = 'linkcube2013@163.com'  
    senderPassword = 'shisong'
    receiver = email
    subject  = 'no-reply'
    # 邮件内容
    # msg = MIMEText('你好','text','utf-8')#中文需参数‘utf-8’，单字节字符不需要 
    msg = MIMEText('<html><p>Your password of skea is:' + password + '</p></html>', 'html', 'utf-8')  # html格式的邮件
    # 邮件主题
    msg['Subject'] = Header(subject, 'utf-8')
    # 发送邮件
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(senderUsername, senderPassword)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()

if __name__=='__main__':
    sendPassword('31@qq.com', '12345678')
