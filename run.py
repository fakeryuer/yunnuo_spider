# coding   : utf-8
# @Time    : 2019/8/15 9:55
# @File    : run.py
# @Software: PyCharm


from p1_myspider import It_Manager
from p2_logined import Logined
import os


# os.chdir('D：\jt_send_mail')
# os.chdir('/Users/yunnuotest/Downloads/jt_send_mail')
print(os.getcwd())
os.chdir(os.getcwd())


# n=截图次数，interval=时间间隔 （秒）
__n = 7
__interval = 3
__to_addr = ['xxxx@xxx.com', ] # 'xxx@xx.net'


if __name__ == '__main__':
    # 1 登陆获取cookies
    # itmanager = It_Manager()
    # itmanager.run()
    # 2 登陆获取数据，发送邮件
    save = Logined()
    save.run(__n, __interval, __to_addr)
