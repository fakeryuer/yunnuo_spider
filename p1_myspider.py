# Python-anaconda3/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2019/1/21 9:01
# @Author  : yuhaoyu
# @Email   : 2384810678@qq.com
# @File    : p1_myspider.py
# @Software: PyCharm

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from io import BytesIO
import time
import datetime
import os
from chaojiying import Chaojiying_Client
import json
from retry import retry


# 获取保持登陆的cookies
class It_Manager(object):

    def __init__(self):
        # 实例化一个浏览器启动参数对象
        self.options = Options()
        # 窗口大小
        self.options.add_argument('--window-size=1366,768')
        self.options.add_argument('--disable-infobars')
        # 添加UA
        self.options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"')

    def start(self):
        # 初始化对象,指定chrome路径
        self.browser = webdriver.Chrome(chrome_options=self.options, executable_path='chromedriver.exe')

        # 远程ubuntu配置
        # self.browser = webdriver.Chrome(chrome_options=self.options, executable_path='/home/chromedriver')
        # self.browser = webdriver.Chrome(chrome_options=self.options, executable_path='/home/chromedriver')  # 如果没有把chromedriver加入到PATH中，就需要指明路径

        self.browser.get('https://117.136.129.122/cmnet/main.htm')

        # 页面刷新
        self.browser.refresh()
        # 验证码----
        image = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="validateCode"]')
        ))
        loc = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="validateCode"]')
        )).location
        # 截屏
        # self.browser.get_screenshot_as_file('screenshot.png')
        window_screen = self.browser.get_screenshot_as_png()
        window_screen = Image.open(BytesIO(window_screen))
        # 截取验证码的位置
        sc = 1.25 # 屏幕显示的比例大小
        x = int(loc['x']*sc)
        y = int(loc['y']*sc)
        print('验证码的位置：',x ,y)
        box = (x, y, x + 59*sc, y + 20*sc)
        test = window_screen.crop(box)
        # test.show()

        # 图片以byte形式储存
        capticha = BytesIO()
        # format指定保存格式
        test.save(capticha, format('png'))
        # 获取图片的二进制数据
        return capticha.getvalue()

    # 把图片传给超级鹰,返回验证字符
    def post_image_get_position(self, captcha):
        cjy = Chaojiying_Client('fakeryu', 'chaojiying', '897644')
        # 验证码Byte传入
        result_string = cjy.PostPic(captcha, 1902).get('pic_str')
        title = '{}.png'.format(result_string)

        # 记录识别的验证码
        yzm  = './yzm_save'
        if not os.path.exists(yzm):
            os.mkdir(yzm)
        os.chdir(yzm)
        # 将验证码写入
        with open(title, 'wb+') as p:
            p.write(captcha)
        os.chdir('..') # 切换到上一级目录

        # 记录识别的验证码
        with open('captcha.txt', 'a+', encoding= 'utf-8') as f:
            f.write('本次{}识别的验证码为{}\n'.format(datetime.datetime.now() ,result_string))

        print(result_string)
        return result_string

    # 登陆信息输入
    def login(self, result_string=None):
        # 显式等待,等待登陆出现
        user = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="name"]')
        ))

        psw = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="pwd"]')
        ))
        yzm = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="exPwd"]')
        ))
        # 登陆信息
        user.clear()
        psw.clear()
        # yzm.clear()
        user.send_keys('xxxxxxxx')
        psw.send_keys('xxxxxxxx')
        yzm.send_keys('{}'.format(result_string))
        #登陆按钮
        button = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located(
            (
            By.XPATH, '/html/body/table/tbody/tr/td/table/tbody/tr[4]/td/table/tbody/tr[3]/td[1]/img')
        ))
        button.click()

    # 获取cookies
    def get_information(self):
        # 流量分析 part1
        part1 = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/ul/li[2]/a')
        ))
        part1.click()
        print('登陆成功，可以进行提取数据')
        cookies = './cookies.txt'
        with open(cookies, 'w+') as f:
            json.dump(self.browser.get_cookies(), f)
        print('成功保存cookies')

    # 主运行程序
    @retry()
    def run(self):
        capticha = self.start()     # 创建浏览器
        result_string = self.post_image_get_position(capticha)  # 获取验证码
        time.sleep(3)
        self.login(result_string)   # 登陆
        self.get_information()    #登陆成功后获取cookies
        self.browser.quit()

if __name__ == '__main__':
    itmanager = It_Manager()
    itmanager.run()