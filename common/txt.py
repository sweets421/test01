# coding=utf-8
from common import logger


class Txt:
    """
    powered by Jhx at 2020/1/26
    用来读写文件
    """

    def __init__(self, path, m='r', coding='gbk'):  # 这里用utf8编码会报错，不知道为什么
        """
        初始化实例，打开一个txt文件
        :param path:文件路径
        :param m:打开文件的方式，r：只读（默认），w：只写，rw：可读写
        :param coding:打开文件的编码，默认utf8
        """
        self.data = []
        self.f = None
        if m == 'r':
            # 逐行读取
            for line in open(path, encoding=coding):
                self.data.append(line)
            for i in range(self.data.__len__()):
                # self.data[i] = self.data[i].encode('utf8').decode('utf-8-sig')  # 处理非法字符
                self.data[i] = self.data[i].replace('\n', '')  # 去掉末尾换行
            return

        if m == 'w':
            # 打开可读文件
            self.f = open(path, 'a', encoding=coding)
            return

        if m == 'rw':
            for line in open(path, encoding=coding):
                self.data.append(line)
            for i in range(self.data.__len__()):
                self.data[i] = self.data[i].encode('utf-8').decode('utf-8-sig')  # 处理非法字符
                self.data[i] = self.data[i].replace('\n', '')
            self.f = open(path, 'a', encoding=coding)
            return

    def read(self):
        """
        将txt文件按行读取为列表
        :return:返回txt所有内容的列表
        """
        return self.data

    def writeline(self, s):
        """
        往txt文件末尾写入一行
        :param s:需要写入的内容
        :return:
        """
        if self.f is None:
            logger.error('未打开可写入txt文件')
            return
        self.f.write(str(s))

    def save_close(self):
        """
        写入文件后，必须要保存
        :return:
        """
        if self.f is None:
            logger.error('未打开可写入txt文件')
            return
        self.f.close()

# if __name__ == '__main__':
#     # 读取
#     reader = Txt('../lib/conf.properties')
#     t = reader.read()
#     print(t)
#     # 写入
#     writer = Txt('../lib/temp.log', m='w')
#     writer.writeline('写入成功\n')
#     writer.save_close()
