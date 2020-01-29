# coding=utf-8
import requests, json
from common import logger

class HTTP:
    """
    powered by Jhx at 2020/1/24
    用于HTTP协议的接口，是关键字库
    """

    def __init__(self, w):
        self.session = requests.session()
        self.result = ''
        self.result_json = {}
        self.result_return = {}
        self.url = ''
        self.writer = w

    def seturl(self, u):
        """
        powered by Jhx at 2020/1/24
        请求的url
        :param u:请求url的host地址
        :return:
        """
        if u.startswith('http') or u.startswith('https'):
            self.url = u
            self.writer.write(self.writer.row, 7, 'PASS')
            self.writer.write(self.writer.row, 8, self.url)
        else:
            logger.error('url格式错误！')
            self.writer.write(self.writer.row, 7, 'FAIL')
            self.writer.write(self.writer.row, 8, 'url格式错误')

    def post(self, url, d=None, js=None):
        """
        powered by Jhx at 2020/1/24
        用于发送post请求
        :param url: 请求路径
        :param d:请求数据，非json格式
        :param js:请求数据，json格式
        :return:
        """
        # 读取Excel文件里面的入参
        if not (url.startswith('http') or url.startswith('https')):
            url = self.url + '/' + url

        if d is None or d == '':
            pass
        else:
            d = self.__get_value(d)
            d = self.__get_data(d)
        res = self.session.post(url, d, js)
        self.result = res.content.decode('utf8')
        try:
            self.result_json = json.loads(self.result)
            self.writer.write(self.writer.row, 7, 'PASS')
            self.writer.write(self.writer.row, 8, str(self.result_json))
        except Exception as e:
            self.result_json = {}
            self.writer.write(self.writer.row, 7, 'FAIL')
            self.writer.write(self.writer.row, 8, str(self.result))

    def removeheader(self, key):
        """
        powered by Jhx at 2020/1/24
        删除请求头中的键值
        :param key: 要删除的键
        :return:
        """
        try:
            del self.session.headers[key]
            self.writer.write(self.writer.row, 7, 'PASS')
            self.writer.write(self.writer.row, 8, str(self.session.headers))
        except Exception as e:
            logger.error("没有" + key + "这个键的header存在")
            self.writer.write(self.writer.row, 7, 'FAIL')
            self.writer.write(self.writer.row, 8, str(self.session.headers))

    def addheader(self, key, value):
        """
        powered by Jhx at 2020/1/24
        添加请求头
        :param key:请求头的键
        :param value: 请求头的值
        :return:
        """
        value = self.__get_value(value)
        self.session.headers[key] = value
        self.writer.write(self.writer.row, 7, 'PASS')
        self.writer.write(self.writer.row, 8, str(self.session.headers))

    def assertequals(self, key, value):
        """
        powered by Jhx at 2020/1/24
        断言
        :param key: 需要断言的返回参数的键
        :param value: 需要断言的返回参数的值
        :return:
        """
        value = self.__get_value(value)
        try:
            if (str(self.result_json[key]) == str(value)):
                logger.info('PASS')
                self.writer.write(self.writer.row, 7, 'PASS')
                self.writer.write(self.writer.row, 8, str(self.result_json[key]))
            else:
                logger.info('FAIL')
                self.writer.write(self.writer.row, 7, 'FAIL')
                self.writer.write(self.writer.row, 8, str(self.result_json[key]))
        except Exception as e:
            logger.exception(e)

    def savejson(self, key, rekey):
        """
        powered by Jhx at 2020/1/24
        保存结果，用于接口之间的关联，将上一接口的返回参数保存下来，在之后的接口中用作入参或者请求头
        :param key: 参数的键
        :param rekey: 参数的值
        :return:
        """
        try:
            self.result_return[rekey] = self.result_json[key]
            self.writer.write(self.writer.row, 7, 'PASS')
            self.writer.write(self.writer.row, 8, str(self.result_return[rekey]))
        except Exception as e:
            logger.error("保存参数失败！没有" + key + "这个键")
            self.writer.write(self.writer.row, 7, 'FAIL')
            self.writer.write(self.writer.row, 8, str(self.result_json))

    def __get_value(self, value):
        """
        powered by Jhx at 2020/1/24
        用于获取{param}参数的值，为私有函数，主要用于接口之间的关联
        :param value: 需要替换的参数
        :return: 返回替换后的值
        """
        try:
            for i in self.result_return:
                value = value.replace('{' + i + '}', self.result_return[i])
        except Exception as e:
            pass
        return value

    def __get_data(self, value):
        """
        powered by Jhx at 2020/1/24
        用于获取数据，如将json字符串转换为字典
        :param value: 传参
        :return: 返回解析后的字典
        """
        param = {}
        try:
            p1 = value.split('&')
            for p2 in p1:
                p3 = p2.split('=')
                param[p3[0]] = p3[1]
        except Exception as e:
            logger.info("参数暂时没法处理！")

        return param
