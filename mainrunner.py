# coding=utf-8
from modules.http import HTTP
from modules.browser import Browser
from common.Excel import *
from common import logger, config
from common.excelresult import Res
from common.mail import Mail
from common.mysql import Mysql

import time
import inspect

"""
powered by Jhx at 2020/1/24
这是整个自动化框架的主代码运行入口
"""


def runcase(line, http):
    global starttime, endtime
    starttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    if len(line[0]) > 0 or len(line[1]) > 0:  # 分组信息，不用执行
        endtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        return
    func = getattr(http, line[3])  # 反射获取函数
    args = inspect.getfullargspec(func).__str__()  # 反射获取关键字参数
    args = args[args.find('args=') + 5:args.rfind(', varargs=')]
    args = eval(args)
    args.remove('self')
    # 若函数没有参数，就返回
    if len(args) == 0:
        func()
        endtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        return
    # 若函数只有一个参数，就读取Excel表格中第五列的入参
    elif len(args) == 1:
        func(line[4])
        endtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        return
    # 若函数有2个参数，就读取Excel表格中第五列的入参
    elif len(args) == 2:
        func(line[4], line[5])
        endtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        return
    # 若函数有3个参数，就读取Excel表格中第五列的入参
    elif len(args) == 3:
        func(line[4], line[5], line[6])
        endtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        return
    else:
        logger.warn("目前最多支持3个参数！")
        endtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))


case_path = './lib/Web用例.xls'
result_path = './lib/result-Web用例.xls'
conf_path = './lib/conf.properties'

reader = Reader()
reader.open_excel(case_path)
sheetnames = reader.get_sheets()

#读取配置文件
config.get_config(conf_path)
logger.info(config.config)

#数据库初始化
# mysql=Mysql()
# mysql.init_mysql(sql_path)

writer = Writer()
writer.copy_open(case_path, result_path)

reader.readline()
http = None
casetype = reader.readline()[1]
if casetype == 'HTTP':
    http = HTTP(writer)
if casetype == 'WEB':
    http = Browser(writer)

for sheet in sheetnames:
    reader.set_sheet(sheet)
    # 保持读写在同一个sheet页面
    writer.set_sheet(sheet)
    for i in range(reader.rows):
        writer.row = i
        line = reader.readline()
        runcase(line, http)

writer.save_close()

# 解析结果，得到报告数据
res = Res()
r = res.get_res(result_path)
logger.info(r)

# 读取配置文件
config.get_config(conf_path)
logger.info(config.config)

# 修改邮件数据
html = config.config['mailtxt']
html = html.replace('title', r['title'])
html = html.replace('status', r['status'])
if r['status'] == "Fail":
    html = html.replace('#00d800', 'red')
html = html.replace('runtype', r['runtype'])
html = html.replace('passrate', r['passrate'])
html = html.replace('casecount', r['casecount'])
html = html.replace('starttime', str(starttime))
html = html.replace('endtime', str(endtime))

# 发送邮件
config.get_config(conf_path)
logger.debug(config.config)
mail = Mail()
mail.send(html)
