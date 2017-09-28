#!python3

'''
对已爬取的4589部电影进行清洗

author: justZero
email: alonezero@foxmail.com
date: 2017-8-7
'''

import re
import time
import pandas as pd
from pandas import Series
from constant import NAME_MAP


def m_clean(movie):
    movie = dict(movie)

    # 去除空白字符
    movie['composer'] = clear_whitespace(movie['composer'])
    movie['actor']    = clear_whitespace(movie['actor'])
    movie['category'] = clear_whitespace(movie['category'])
    movie['language'] = clear_whitespace(movie['language'])
    movie['othername'] = clear_whitespace(movie['othername'])

    # 发行地区去重，通过统一的映射字典命名
    district = movie['district'].split('/')[0].strip()
    movie['district'] = NAME_MAP.get(district, '未知')

    # 上映时间只取年份
    movie['showtime'] = movie['showtime'][:4]

    # 时长只取数字（单位：分钟）
    # -1表示无时长数据
    length = re.findall(r'(\d+)\s*分钟', movie['length'])
    movie['length'] = length[0] if len(length) > 0 else '-1'

    # 简介的段分隔符改为'/'
    movie['description'] = movie['description'].replace('\t', '/')

    return Series(movie)      

# 清除字符串中的空白字符：空格、制表符等
def clear_whitespace(str):
    return re.sub(r'\s+', '', str)

if __name__ == '__main__':
    inputFile = 'data/douban_movie_detail.txt'
    outputFile = 'data/douban_movie_clean.txt'

    movies_df = pd.read_csv(inputFile, sep='^')
    movies = movies_df.apply(m_clean, axis=1)

    cols = ['id','title','url','cover','rate','director', 'composer','actor','category','district','language','showtime','length','othername','description']
    movies.to_csv(outputFile, sep='^', index=False, encoding='utf-8', columns=cols)
