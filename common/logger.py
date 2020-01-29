# coding=utf-8
import logging

"""
powered by Jhx at 2020/1/26
用来格式化打印日志到文件和控制台
"""
path = '.'
formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(message)s')
# create file handler and set level to debug
c = logging.FileHandler(path + "/lib/all.log", mode='a', encoding='utf8')
logger = logging.getLogger('frame log')
logger.setLevel(logging.DEBUG)
c.setFormatter(formatter)
logger.addHandler(c)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)


# 打印debug级别日志
def debug(ss):
    global logger
    try:
        logger.debug(str(ss))
    except:
        return


# 打印info级别日志
def info(ss):
    global logger
    try:
        logger.info(str(ss))
    except:
        return


# 打印warn级别日志
def warn(ss):
    global logger
    try:
        logger.warn(str(ss))
    except:
        return


# 打印error级别日志
def error(ss):
    global logger
    try:
        logger.error(str(ss))
    except:
        return


# 打印异常日志
def exception(e):
    global logger
    try:
        logger.exception(str(e))
    except:
        return


# if __name__ == '__main__':
#     debug('test')
