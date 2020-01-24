# coding=utf-8
from modules.http import HTTP
from common.Excel import *
import inspect

"""
powered by Jhx at 2020/1/24
这是整个自动化框架的主代码运行入口
"""


def runcase(line, http):
    if len(line[0]) > 0 or len(line[1]) > 0:  # 分组信息，不用执行
        return
    func = getattr(http, line[3])  # 反射获取函数
    args = inspect.getfullargspec(func).__str__()  # 反射获取关键字参数
    args = args[args.find('args=') + 5:args.rfind(', varargs=')]
    args = eval(args)
    args.remove('self')
    # 若函数没有参数，就返回
    if len(args) == 0:
        func()
        return
    # 若函数只有一个参数，就读取Excel表格中第五列的入参
    elif len(args) == 1:
        func(line[4])
        return
    # 若函数有2个参数，就读取Excel表格中第五列的入参
    elif len(args) == 2:
        func(line[4], line[5])
        return
    # 若函数有3个参数，就读取Excel表格中第五列的入参
    elif len(args) == 3:
        func(line[4],line[5],line[6])
        return
    # 若函数有4个参数，就读取Excel表格中第五列的入参
    elif len(args) == 4:
        func(line[4],line[5],line[6],line[7])
        return
    else:
        print("目前最多支持4个参数！")

file_path='./lib/HTTP接口用例.xls'


reader = Reader()
reader.open_excel(file_path)
sheetnames = reader.get_sheets()

writer = Writer()
writer.copy_open(file_path, './lib/result-HTTP接口用例.xls')
http=HTTP(writer)


for sheet in sheetnames:
    reader.set_sheet(sheet)
    #保持读写在同一个sheet页面
    writer.set_sheet(sheet)
    for i in range(reader.rows):
        writer.row=i
        line=reader.readline()
        runcase(line,http)

writer.save_close()
