#!python3

"""
为爬虫运行提供日志功能

author: justZero
email: alonezero@foxmail.com
date: 2017-8-8
"""

import logging


class Logger(object):

    def __init__(self, name, logname):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        format_pattern = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
        # handler 用于输出到文件
        fileHandler = logging.FileHandler(filename='log/'+logname,
                                          mode='a',
                                          encoding='utf8')
        ffmt = logging.Formatter(format_pattern)
        fileHandler.setFormatter(ffmt)

        # 再来一个 hanlder 用于输出到控制台
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        cfmt = logging.Formatter(format_pattern)
        console.setFormatter(cfmt)

        self.logger.addHandler(fileHandler)
        self.logger.addHandler(console)

    def error(self, msg):
        self.logger.error(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def exception(self, msg):
        self.logger.exception(msg)


if __name__ == '__main__':
    logger = Logger('test', 'test.log')

    logger.debug('调试信息')
    logger.info('提示信息')
    logger.warning('警告信息')
    logger.error('错误信息')

    try:
        None.do() # 异常代码
    except Exception as e:
        logger.exception("出了一些问题...")
