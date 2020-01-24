# coding=utf-8
import xlrd, xlwt, traceback
from xlutils.copy import copy


class Reader:
    """
    powered by Jhx at 2020/1/24
    用来读取Excel文件内容
    目前暂不支持xlsx的excel，可以将xlsx另存为xls，不能只是改扩展名
    """

    def __init__(self):
        # 先将Excel文件读取到内存，然后依次遍历行
        self.workbook = None  # 整个Excel工作薄缓存
        self.sheet = None  # 当前工作sheet
        self.rows = 0  # 当前sheet页的总行数
        self.r = 0  # 当前读取到的行数

    def open_excel(self, srcfile):
        # 打开Excel
        xlrd.Book.encoding = "utf8"  # 设置读取的Excel使用utf-8编码
        self.workbook = xlrd.open_workbook(filename=srcfile)  # 读取Excel的内容到缓存的workbook
        self.sheet = self.workbook.sheet_by_index(0)  # 读取第一个sheet页面
        self.rows = self.sheet.nrows  # 设置rows为当前sheet的行数
        self.r = 0  # 设置默认读取为第一行
        return

    def get_sheets(self):
        # 获取sheet页面
        sheets = self.workbook.sheet_names()  # 获取所有sheet的名字，并返回为一个列表
        return sheets

    def set_sheet(self, name):
        # 切换sheet页面
        self.sheet = self.workbook.sheet_by_name(name)  # 通过sheet名字，切换sheet页面
        self.rows = self.sheet.nrows
        self.r = 0
        return

    def readline(self):
        # 逐行读取
        # 如果当前还没读取到最后一航，则往下读取一行
        if (self.r < self.rows):
            row = self.sheet.row_values(self.r)  # 读取第r行的内容
            self.r = self.r + 1  # 设置下一次读取r的下一行
        return row


class Writer:
    """
    powered by Jhx at 2020/1/24
    用来复制写入Excel文件
    """

    def __init__(self):
        # 先将内容写入到内存，然后保存到Excel文件
        self.workbook = None  # 读取需要复制的Excel
        self.wb = None  # 拷贝的工作空间
        self.sheet = None  # 当前工作sheet
        self.df = None  # 记录生成的文件，用来保存
        self.row = 0  # 记录写入的行
        self.col = 0  # 记录写入的列

    def copy_open(self, srcfile, dstfile):
        # 写入excel过程：读取结果->复制用例文件的workbook->结果写入内存workbook里面->保存到新文件
        self.df = dstfile
        self.workbook = xlrd.open_workbook(filename=srcfile, formatting_info=True)  # formatting_info带格式的复制
        self.wb = copy(self.workbook)
        return

    def get_sheets(self):
        # 获取sheet页面
        sheets = self.workbook.sheet_names()  # 获取所有sheet的名字，并返回为一个列表
        return sheets

    def set_sheet(self, name):
        # 切换sheet页面
        self.sheet = self.wb.get_sheet(name)  # 通过sheet名字，切换sheet页面
        return

    def write(self, r, c, value):
        # 写入指定单元格，保留原格式
        def _getCell(sheet, r, c):  # 获取要写入的单元格
            row = sheet._Worksheet__rows.get(r)  # 获取行
            cell = row._Row__cells.get(c)  # 获取单元格
            return cell

        cell = _getCell(self.sheet, r, c)
        self.sheet.write(r, c, value)  # 写入值
        ncell = _getCell(self.sheet, r, c)
        ncell.xf_idx = cell.xf_idx  # 设置写入后格式和写入前一样

        return

    def save_close(self):
        try:
            self.wb.save(self.df)  # 保存复制后的文件到硬盘
        except Exception as e:
            print(traceback.format_exc(e))
        return


# if __name__ == '__main__':
#     reader = Reader()
#     reader.open_excel('../lib/HTTP接口用例.xls')
#     sheetnames = reader.get_sheets()
#     for sheet in sheetnames:
#         reader.set_sheet(sheet)
#         for i in range(reader.rows):
#             print(reader.readline())
#
#     writer = Writer()
#     writer.copy_open('../lib/HTTP接口用例.xls', '../lib/result-HTTP接口用例.xls')
#     sheetnames = writer.get_sheets()
#     writer.set_sheet(sheetnames[0])
#     writer.write(1, 1, 'jhx-test')
#     writer.save_close()
