# coding=utf-8
from selenium.webdriver import *
from selenium.webdriver.common.action_chains import ActionChains
from common import logger
import os, time, traceback


class Browser:
    """
    powered by Jhx at 2020/1/29
    用于web自动化的关键字库
    """

    def __init__(self, w):
        self.driver = None
        self.title = ''
        self.text = ''
        self.writer = w

    def openbrowser(self, browser='Chrome', dr=None):
        if browser == 'Chrome' or browser == '':
            if dr == None or dr == '':
                dr = "./lib/chromedriver.exe"
            # 创建一个用来配置Chrome属性的变量
            Options = ChromeOptions()
            # 去掉"Chrome正受到自动测试软件的控制"字样
            Options.add_experimental_option("excludeSwitches", ['enable-automation'])
            # 加载缓存
            user_profile = os.environ['USERPROFILE']
            Options.add_argument(
                '--user-data-dir=' + user_profile + '\\AppData\\Local\\Google\\Chrome\\User Data\\')
            # 打开谷歌浏览器
            self.driver = Chrome(executable_path=dr, options=Options)
            self.writer.write(self.writer.row, 7, 'PASS')
            self.writer.write(self.writer.row, 8, 'Chrome浏览器打开成功')
        elif browser == 'Firefox':
            if dr == None or dr == '':
                dr = '../lib/geckodriver.exe'
            # 打开火狐浏览器
            self.driver = Firefox(executable_path=dr)
            self.writer.write(self.writer.row, 7, 'PASS')
            self.writer.write(self.writer.row, 8, 'Firefox浏览器打开成功')
        elif browser == 'ie':
            if dr == None or dr == '':
                dr = '../lib/IEDriverServer.exe'
            # 打开ie浏览器
            self.driver = Ie(executable_path=dr)
            self.writer.write(self.writer.row, 7, 'PASS')
            self.writer.write(self.writer.row, 8, 'IE浏览器打开成功')
        else:
            logger.warn("该浏览器暂未实现自动化功能!")
            self.writer.write(self.writer.row, 7, 'FAIL')
            self.writer.write(self.writer.row, 8, '该浏览器暂未实现自动化功能')
        return

    def geturl(self, url):
        # 访问指定网页
        try:
            self.driver.get(url)
            self.writer.write(self.writer.row, 7, 'PASS')
            self.writer.write(self.writer.row, 8, '网站访问成功')
        except Exception as e:
            self.writer.write(self.writer.row, 7,'FAIL')
            self.writer.write(self.writer.row, 8,traceback.format_exc())

    def wait(self, t=10):
        if t=='':
            t=10
        self.driver.implicitly_wait(t)
        self.writer.write(self.writer.row, 7, 'PASS')
        self.writer.write(self.writer.row, 8, '')

    def sleep(self, t=3):
        if t=='':
            t=3
        time.sleep(t)
        self.writer.write(self.writer.row, 7, 'PASS')
        self.writer.write(self.writer.row, 8, '')

    def swithwindow(self, idx=0):
        h = self.driver.window_handles
        self.driver.switch_to.window(h[int(idx)])
        self.writer.write(self.writer.row, 7, 'PASS')
        self.writer.write(self.writer.row, 8, '切换窗口成功')

    def gettitle(self):
        # 获取窗口名称
        self.title = self.driver.title
        self.writer.write(self.writer.row, 7, 'PASS')
        self.writer.write(self.writer.row, 8, '窗口名称获取成功')

    def closewindow(self):
        self.driver.close()
        self.writer.write(self.writer.row, 7, 'PASS')
        self.writer.write(self.writer.row, 8, '窗口关闭成功')

    def click(self, xpath):
        self.driver.find_element_by_xpath(xpath).click()
        self.writer.write(self.writer.row, 7, 'PASS')
        self.writer.write(self.writer.row, 8, '点击操作成功')

    def input(self, xpath, value):
        self.driver.find_element_by_xpath(xpath).send_keys(str(value))
        self.writer.write(self.writer.row, 7, 'PASS')
        self.writer.write(self.writer.row, 8, '输入操作成功')

    def moveto(self, xpath):
        actions = ActionChains(self.driver)
        actions.move_to_element(self.driver.find_element_by_xpath(xpath)).perform()
        self.writer.write(self.writer.row, 7, 'PASS')
        self.writer.write(self.writer.row, 8, '滑动操作成功')

    def executejs(self, js):
        self.driver.execute_script(js)
        self.writer.write(self.writer.row, 7, 'PASS')
        self.writer.write(self.writer.row, 8, '滑动操作成功')

    def gettext(self, xpath):
        self.text = self.driver.find_element_by_xpath(xpath).text
        self.writer.write(self.writer.row, 7, 'PASS')
        self.writer.write(self.writer.row, 8, '获得文本成功')

    def intoiframe(self, xpath):
        self.driver.switch_to.frame(self.driver.find_element_by_xpath(xpath))
        self.writer.write(self.writer.row, 7, 'PASS')
        self.writer.write(self.writer.row, 8, '进入iframe成功')

    def outiframe(self):
        self.driver.switch_to.default_content()
        self.writer.write(self.writer.row, 7, 'PASS')
        self.writer.write(self.writer.row, 8, '回到主frame成功')

    def assertequals(self, key, value):
        try:
            key = key.replace('{text}', self.text)
            key = key.replace('{title}', self.title)
            if str(key) == str(value):
                self.writer.write(self.writer.row, 7, 'PASS')
                self.writer.write(self.writer.row, 8, '校验成功')
            else:
                self.writer.write(self.writer.row, 7, 'FAIL')
                self.writer.write(self.writer.row, 8, '校验失败')
        except Exception as e:
            self.writer.write(self.writer.row, 7, 'FAIL')
            self.writer.write(self.writer.row, 8, traceback.format_exc())

    def quit(self):
        # 关闭浏览器
        self.driver.quit()
        self.writer.write(self.writer.row, 7, 'PASS')
        self.writer.write(self.writer.row, 8, '浏览器关闭成功')
