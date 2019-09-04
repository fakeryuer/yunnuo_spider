# Python-anaconda3/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2019/1/23 20:38
# @Author  : yuhaoyu
# @Email   : 2384810678@qq.com
# @File    : p2_logined.py
# @Software: PyCharm

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import os
import json
import yagmail


# n=截图次数，interval=时间间隔 （秒）
# __n = 7
# __interval = 3600
# __to_addr = ['2384810678@qq.com', 'panhy@yunochina.net']

# 添加保存的cookie直接登陆
class Logined(object):

    def __init__(self):
        # 实例化一个浏览器启动参数对象
        self.options = Options()
        # 窗口大小
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--disable-infobars')
        # 无界面运行
        # self.options.add_argument('--headless')
        # 添加UA
        self.options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/68.0"')

    def start(self):
        # 初始化对象,指定chrome路径
        self.browser = webdriver.Chrome(chrome_options=self.options, executable_path='chromedriver.exe')

        self.browser.get('https://www.baidu.com/')

        with open('cookies.txt') as f:
            cookies = json.load(f)
        print(cookies)
        for cookie in cookies:      # cookies必须以json形式；每次加入一个
            self.browser.add_cookie(cookie)
        self.browser.get('https://117.136.129.122/cmnet/main.htm')

    def get_information(self):
        # 流量分析 part1
        part1 = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/ul/li[2]/a')
        ))
        part1.click()
        print('登陆成功，可以进行提取数据')
        with open('./cookies.txt', 'w+') as f:
            json.dump(self.browser.get_cookies(), f)
        # 全局分析
        part2 = WebDriverWait(self.browser, 300).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="menu5"]/li[1]')
        ))
        part2.click()
        # 链路流量
        part3 = WebDriverWait(self.browser, 300).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="root-menu-div"]/div[2]/ul/li/div/span')
        ))
        part3.click()

        # 切换frame窗口
        self.browser.switch_to_frame("Main_Page")
        # 管理域:浙江骨干
        part4 = WebDriverWait(self.browser, 300).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="domainId"]/option[14]')
        ))
        part4.click()

        # 时间选择
        time1 = datetime.datetime.now()
        time2 = time1 + datetime.timedelta(days=1)
        input_time1 = time1.strftime("%Y-%m-%d")
        input_time2 = time2.strftime("%Y-%m-%d")

        starttime = WebDriverWait(self.browser, 300).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="beginDate"]')
        ))
        starttime.clear()
        starttime.send_keys(input_time1)
        print('查询起始时间', input_time1)

        endtime = WebDriverWait(self.browser, 300).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="endDate"]')
        ))
        endtime.clear()
        endtime.send_keys(input_time2)
        print('查询结束时间', input_time2)
        
        # 查询按钮
        query = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="form1"]/table/tbody/tr[2]/td[1]/table/tbody/tr[2]/td/table/tbody/tr/td[1]/input')
        ))
        # 设备组：
        zu_all = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="ipt_devGrpId"]')
        ))
        # zu_all.click()
        # 骨干电信互联
        zu1 = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="devGrpId"]/option[5]')
        ))
        # zu1.click()
        # query.click()

        # 骨干联通互联
        # zu_all.click()
        zu2 = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="devGrpId"]/option[9]')
        ))
        # zu2.click()
        # query.click()

        # 截屏文件保存路径
        send_data = './send_data/{}'.format(datetime.datetime.now().strftime('%Y-%m-%d'))
        print(send_data)
        if not os.path.exists(send_data):  # 创建当前查询的截图文件
            os.mkdir(send_data)
        os.chdir(send_data)
        print('截图保存路径--', os.getcwd())
        os.chdir('..')
        os.chdir('..')

        return query, zu_all, zu1, zu2, send_data


    def how_times(self, n, interval, __to_addr, *args):
        query, zu_all, zu1, zu2, send_data = args[0]  # 一定要索引下标【0】
        for i in range(0, n):
            try:
                # 骨干电信互联
                print('第{}次截图'.format(i+1))
                zu_all.click()
                zu1.click()
                query.click()
                os.chdir(send_data)
                pic1 = 'dianxin{}.png'.format(i)
                self.browser.get_screenshot_as_file(pic1)

                # 骨干联通互联
                zu_all.click()
                zu2.click()
                query.click()
                pic2 = 'liantong{}.png'.format(i)
                self.browser.get_screenshot_as_file(pic2)

                os.chdir('..')
                os.chdir('..')

                # 发送邮件
                times = datetime.datetime.now()
                paths = './send_data/{}/'.format(times.strftime("%Y-%m-%d"))
                path2 = '{}dianxin{}.png'.format(paths, i)
                path3 = '{}liantong{}.png'.format(paths, i)
                print('图片路径',paths,path2,path3)
                emails = Send_email(__to_addr)
                if os.path.exists(path2) and os.path.exists(path3):
                    print('文件存在')
                    emails.send_mails(i + 1, path2, path3)
            except Exception as e:
                pass
            # 截图时间间隔
            time.sleep(interval)

    def run(self, n, interval, __to_addr):
        self.start()
        returns = self.get_information()
        self.how_times(n, interval,  __to_addr, returns) # returns放在最后
        self.browser.quit()


class Send_email(object):

    def __init__(self, __to_addr):
        # 用户信息
        self.from_addr = 'yuhy@yunochina.net'
        self.password = 'EPK4WfKQ2MYaJ8n7'  # 腾讯QQ邮箱或腾讯企业邮箱必须使用授权码进行第三方登陆
        self.smtp_server = 'smtp.exmail.qq.com'
        # 收件人信息
        self.to_addr = __to_addr
        # #链接邮箱服务器
        self.yag = yagmail.SMTP(user=self.from_addr, password=self.password, host=self.smtp_server)


    def send_mails(self, n, f1, f2):
        # 邮箱正文
        subject = '网络全景可视化管控系统,第{}次发送,{}'.format(n, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        contents = '发送时间{}\n --- Send by Python'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        # 邮件构造
        self.yag.send(self.to_addr, subject, contents, [f1, f2])



# if __name__ == '__main__':
#     save =  Logined()
#     save.run(__n, __interval,__to_addr)
