# coding=utf-8
from selenium.webdriver import *
import time, os


class Browser:
    def __init__(self):
        self.driver = None

    def openbrowser(self, browser='Chrome', driver=None):
        if (browser == 'Chrome'):
            # 创建一个用来配置Chrome属性的变量
            Options = ChromeOptions()
            # 去掉"Chrome正受到自动测试软件的控制"字样
            Options.add_experimental_option("excludeSwitches", ['enable-automation'])
            # 加载缓存
            user_profile = os.environ['USERPROFILE']
            Options.add_argument(
                '--user-data-dir=' + user_profile + '\\AppData\\Local\\Google\\Chrome\\User Data\\')
            # 打开谷歌浏览器
            self.driver = Chrome(executable_path="../lib/chromedriver.exe", options=Options)
        elif (browser == 'Firefox'):
            # 打开火狐浏览器
            self.driver = Firefox(executable_path="../lib/geckodriver.exe")
        elif (browser == 'ie'):
            # 打开ie浏览器
            self.driver = Ie(executable_path='../lib/IEDriverServer.exe')
        else:
            print("该浏览器暂未实现自动化功能!")

    def geturl(self, url):
        # 访问指定网页
        self.driver.get(url)

    def quit(self):
        # 关闭浏览器
        self.driver.quit()
