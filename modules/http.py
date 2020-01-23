# coding=utf-8
import requests, json


class HTTP:
    def __init__(self):
        self.session = requests.session()
        self.result = ''
        self.result_json = {}
        self.result_return = {}

    def post(self, url, d=None, js=None, en='utf8'):
        if (d is None):
            pass
        else:
            d = self.__get_value(d)
            d = self.__get_data(d)
        res = self.session.post(url, d, js)
        self.result = res.content.decode(en)
        self.result_json = json.loads(self.result)

    def addheaders(self, key, value):
        value = self.__get_value(value)
        self.session.headers[key] = value

    def assertequals(self, key, value):
        if (str(self.result_json[key]) == str(value)):
            print('PASS')
        else:
            print('FAIL')

    def saveresults(self, key, rekey):
        self.result_return[rekey] = self.result_json[key]

    def __get_value(self, value):
        for i in self.result_return:
            value = value.replace('{' + i + '}', self.result_return[i])
        return value

    def __get_data(self, value):
        param = {}
        p1 = value.split('&')
        for p2 in p1:
            p3 = p2.split('=')
            param[p3[0]] = p3[1]
        return param
