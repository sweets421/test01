# coding=utf-8
from common import logger
from common.txt import Txt

# 全局变量，用来存储配置
config = {}


def get_config(path):
    """
    powered by Jhx at 2020/1/27
    用来将配置文件转换为字典，方便后续使用
    :param path:配置文件路径
    :return:返回配置文件dict
    """
    global config
    config.clear()  # 重新获取时，先清空配置
    txt = Txt(path)
    data = txt.read()
    for s in data:
        if s.startswith('#'):  # 跳过注释
            continue
        if not s.find('='):
            logger.warn('配置文件格式错误，请检查：' + str(s))
            continue
        try:
            key = s[0:s.find('=')]
            value = s[s.find('=') + 1:s.__len__()]
            config[key] = value
        except Exception as e:
            logger.warn('配置文件格式错误，请检查：' + str(s))
            logger.exception(e)

    return config


# if __name__ == '__main__':
#     conf = get_config('../lib/conf.properties')
#     print(conf)
