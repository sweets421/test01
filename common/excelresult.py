# coding=utf-8
from common.Excel import Reader
from common import logger


class Res:
    """
    powered by Jhx at 2020/1/27
    统计Excel用例执行结果信息
    """

    def __init__(self):
        self.summary = {}  # 用于记录所有模块分组信息名称

    def get_res(self, result_path):
        # 用于记录执行统计结果，逻辑为：只要分组中出现一个失败用例，则认为该分组执行失败，与flag联合使用
        self.summary.clear()
        status = "Fail"
        flag = True  # 标志是否有失败
        totalcount = 0  # 统计测试用例集的用例总条数
        totalpass = 0  # 统计所有用例中通过用例的条数

        reader = Reader()
        reader.open_excel(result_path)
        reader.readline()
        line = reader.readline()
        self.summary['runtype'] = line[1]
        self.summary['title'] = line[2]
        self.summary['starttime'] = line[3]
        self.summary['endtime'] = line[4]

        # 获取所有sheet页面
        for n in reader.get_sheets():
            reader.set_sheet(n)  # 从第一个页面开始解析
            row = reader.rows  # 获取sheet的行数，用来遍历
            reader.r = 1  # 设置从第二行开始读

            # 遍历sheet里面所有用例
            for i in range(1, row):
                line = reader.readline()
                # 查找记录了分组信息的行
                # 如果第一列（分组信息）和第二列（类别或用例名）不同时为空，则不是用例，执行非用例的操作
                if not (line[0] == '' and line[1] == ''):
                    pass
                # 非用例行判断结束
                # 第一列信息和第二列信息均为空的行，即用例行，这时开始进行用例数、通过数、状态的统计
                else:
                    # 判断执行结果列，如果为空，将flag置为false，视为该行有误，不纳入用例数量计算
                    if len(line) < 7 or line[7] == '':
                        flag = False
                    # 执行结果不为空，则将用例统计数自增
                    else:
                        totalcount += 1
                        # 如果通过，则通过数和总通过数均自增
                        if line[7] == "PASS":
                            totalpass += 1
                        else:
                            # 出现了用例执行结果不是PASS的情况，则视为当前分组执行失败
                            flag = False

        # 所有用例执行概况
        # 计算执行通过率
        if flag:
            status = "PASS"

        # 计算通过率，百分率
        try:
            p = int(totalpass * 10000 / totalcount)
            passrate = p / 100
        except Exception as e:
            passrate = 0.0
            logger.exception(e)

        # 用例总数
        self.summary['casecount'] = str(totalcount)
        # 通过率
        self.summary['passrate'] = str(passrate)
        self.summary['status'] = status

        return self.summary


# if __name__ == '__main__':
#     res = Res()
#     r = res.get_res('../lib/result-HTTP接口用例.xls')
#     print(r)
