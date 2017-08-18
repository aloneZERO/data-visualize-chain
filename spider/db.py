#!python3

'''
数据库操作类

author: justZero
email: alonezero@foxmail.com
date: 2017-8-6
'''

import time
import pandas as pd
import numpy as np
import pymysql
import pymysql.cursors
import pprint


class MySQLdb(object):

    def __init__(self):
        self.conn = pymysql.connect(
                            host='localhost',
                            user='root',
                            passwd='root',
                            db='douban_movie',
                            port=8889,
                            charset='utf8',
                            cursorclass=pymysql.cursors.DictCursor)

        self.conn.autocommit(True)
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()
        self.cursor.close()

    # 批量插入
    def __insert_many(self, sql, params):
        self.cursor.executemany(sql, params)

    # 电影数据插入
    def insert_movie(self, params):
        sql = 'insert into movie(movieId,title,url,cover,rate,director,composer,actor,category,district,language,showtime,length,othername,description) '+ \
              'values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        self.__insert_many(sql, params)

    # 统计数据插入
    def insert_rate(self, params):
        sql = 'insert into rate(name,category,rate) values(%s,%s,%s)'
        self.__insert_many(sql, params)

if __name__ == '__main__':
    inputFile = 'data/douban_movie_clean.txt'
    movies_df = pd.read_csv(inputFile, sep='^')
    movies = np.array(movies_df).tolist()
    
    db = MySQLdb()
    try:
        db.insert_movie(movies)
    except Exception as e:
        raise e
    finally:
        db.close()
