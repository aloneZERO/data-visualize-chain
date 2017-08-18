#!python3

'''
对清洗后的电影数据进行基本统计,
并根据统计的数据生成json文件或插入数据库中。

author: justZero
email: alonezero@foxmail.com
date: 2017-8-6
'''

import json
import time
import numpy as np
import pandas as pd
from pandas import Series
from db import MySQLdb


# TOP数量统计
def topk(s, k=10):
    col = s.name
    outputFile = '../web/static/data/' + col + '.json'
    s.str.split('/', expand=True) \
         .stack() \
         .reset_index(level=0) \
         .set_index('level_0') \
         .rename(columns={0:col})[col].value_counts().to_json(outputFile)

# 数量统计
# simple为False, 表示该列数据需要展开
# 例：搞笑/动作 => 搞笑 and 动作
def count_f(s, simple=True):
    col = s.name
    outputFile = '../web/static/data/' + col + '.json'
    if not simple:
        s.str.split('/', expand=True) \
             .stack() \
             .reset_index(level=0) \
             .set_index('level_0') \
             .rename(columns={0:col})[col].value_counts().to_json(outputFile)
    else:
        s.value_counts().to_json(outputFile)


if __name__ == '__main__':
    inputFile = 'data/douban_movie_clean.txt'
    outputDir = '../web/static/data/'

    movies_df = pd.read_csv(inputFile, sep='^')

    topk(movies_df['category'])
    topk(movies_df['language'])

    count_f(movies_df['showtime'])
    count_f(movies_df['length'])
    count_f(movies_df['rate'])
    count_f(movies_df['district'])

    # 统计各个区域各个分类的平均评分
    # 先展开分类，然后利用分组计算平均评分
    rate_df = movies_df['category'].str.split('/', expand=True) \
                                        .stack() \
                                        .reset_index(level=0) \
                                        .set_index('level_0') \
                                        .rename(columns={0:'category'}) \
                                        .join(movies_df.drop('category', axis=1))

    rate_res = rate_df.groupby(['district', 'category'], as_index=False)['rate'].min()
    rate_res = np.array(rate_res).tolist() # dataframe to list

    # 将计算的评分数据存入数据库
    db = MySQLdb()
    try:
        db.insert_rate(rate_res)
    except Exception as e:
        raise e
    finally:
        db.close()
