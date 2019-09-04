# Python-anaconda3/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2019/1/21 9:03
# @Author  : yuhaoyu
# @Email   : 2384810678@qq.com
# @File    : p3_send_email.py
# @Software: PyCharm

# Python-anaconda3/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2019/1/21 9:03
# @Author  : yuhaoyu
# @Email   : 2384810678@qq.com
# @File    : p3_send_email.py
# @Software: PyCharm

import time
import datetime
import yagmail
import os


# 用户信息
from_addr = 'yuhy@xxx.net'
password = 'xx'    # 腾讯QQ邮箱或腾讯企业邮箱必须使用授权码进行第三方登陆
smtp_server = 'smtp.exmail.qq.com'
# 收件人信息
to_addr = ['xxx@qq.com', 'xxx@xxxx.net']
# 发送主题

#链接邮箱服务器
yag = yagmail.SMTP(user=from_addr, password=password, host=smtp_server)
# yag.send(to_addr, subject, '测试1', ['send_data\\2019-01-24\dianxin0.png',])

def send_mails(n, f1, f2):
    # print(f1, f2)
    # 邮箱正文
    subject = '网络全景可视化管控系统,第{}次发送,{}'.format(n, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    contents = '发送时间{}\n --- Send by Python'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    # 发送邮件
    yag.send(to_addr, subject, contents, [f1, f2])



time1 = datetime.datetime.now()
path1 = './send_data/{}/'.format(time1.strftime("%Y-%m-%d"))


# n=截图次数，interval=时间间隔
_n=7
_interval=3600
for i in range(_n):
    # print(path1)
    path2 = '{}dianxin{}.png'.format(path1, i)
    path3 = '{}liantong{}.png'.format(path1, i)
    print(path2,'\n',path3)
    # print('path1', path1)
    # print('path2', path2)
    # print('path3', path3)
    print(os.path.exists(path2), '\n', os.path.exists(path3))
    if os.path.exists(path2) and os.path.exists(path3):
        print('文件存在')
        send_mails(i+1, path2, path3)
    time.sleep(_interval+10)
