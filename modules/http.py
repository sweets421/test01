# coding=utf-8
import requests, json


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
            self.writer.write(self.writer.row,7,'PASS')
            self.writer.write(self.writer.row, 8, self.url)
        else:
            print('error:url格式错误！')
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
        self.result_json = json.loads(self.result)
        print(self.result_json)

    def removeheader(self, key):
        """
        powered by Jhx at 2020/1/24
        删除请求头中的键值
        :param key: 要删除的键
        :return:
        """
        try:
            self.session.headers.remove(key)
        except Exception as e:
            print("没有" + key + "这个键的header存在")

    def addheaders(self, key, value):
        """
        powered by Jhx at 2020/1/24
        添加请求头
        :param key:请求头的键
        :param value: 请求头的值
        :return:
        """
        value = self.__get_value(value)
        self.session.headers[key] = value

    def assertequals(self, key, value):
        """
        powered by Jhx at 2020/1/24
        断言
        :param key: 需要断言的返回参数的键
        :param value: 需要断言的返回参数的值
        :return:
        """
        if (str(self.result_json[key]) == str(value)):
            print('PASS')
        else:
            print('FAIL')

    def saveresults(self, key, rekey):
        """
        powered by Jhx at 2020/1/24
        保存结果，用于接口之间的关联，将上一接口的返回参数保存下来，在之后的接口中用作入参或者请求头
        :param key: 参数的键
        :param rekey: 参数的值
        :return:
        """
        self.result_return[rekey] = self.result_json[key]

    def __get_value(self, value):
        """
        powered by Jhx at 2020/1/24
        用于获取{param}参数的值，为私有函数，主要用于接口之间的关联
        :param value: 需要替换的参数
        :return: 返回替换后的值
        """
        for i in self.result_return:
            value = value.replace('{' + i + '}', self.result_return[i])
        return value

    def __get_data(self, value):
        """
        powered by Jhx at 2020/1/24
        用于获取数据，如将json字符串转换为字典
        :param value: 传参
        :return: 返回解析后的字典
        """
        param = {}
        p1 = value.split('&')
        for p2 in p1:
            p3 = p2.split('=')
            param[p3[0]] = p3[1]
        return param
