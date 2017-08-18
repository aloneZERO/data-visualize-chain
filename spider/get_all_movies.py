#!python3

'''
一次性爬取豆瓣所有电影的概要信息

author: justZero
email: alonezero@foxmail.com
date: 2017-8-7
'''

import time
import json
import requests
from logger import Logger
import constant as api


logger = Logger('Spider_get_all_movies', 'spider.log')

# 爬取电影分类标签
def get_movie_tags():
	try:
		r = requests.get(api.MOVIE_TAG_URL, headers=api.HEADERS)
		r.raise_for_status()
	except Exception as e:
		logger.exception("电影分类标签爬取失败")
		return (False, None)
	else:
		tags = json.loads(r.text)['tags']
		logger.info("抓取到的分类标签："+str(tags))
		return (True, tags)

# 爬取全部电影概要信息并存储
def get_all_movies():
	result = {}

	outputFile = 'data/douban_movie.txt'
	with open(outputFile, 'w', encoding='utf8') as fw:
		fw.write('id;title;url;cover;rate\n')

		finished, tags = get_movie_tags()
		if not finished:
			return

		for tag in tags:
			logger.info("当前爬取的电影概要信息的标签: " + tag)
			start = 0
			while True:
				# 获取电影概要信息
				url = api.MOVIE_SUBJECT_URL % (tag, start)
				try:
					r = requests.get(url, headers=api.HEADERS)
					r.raise_for_status()
				except Exception as e:
					logger.exception("电影概要信息爬取失败, URL: "+url)
				else:
					r.encoding = 'utf-8'

					movies = json.loads(r.text)['subjects']
					if len(movies) == 0:
						break
					for item in movies:
						movieId = str(item['id'])
						title = item['title']
						url = item['url']
						cover = item['cover']
						rate = str(item['rate'])

						# 电影去重
						if movieId in result.keys():
							continue
						else:
							result[movieId] = 1

						record = str(movieId)+ ';' +title+ ';' +url+ ';' + cover+ ';' +str(rate) + '\n'
						fw.write(record)
						logger.info(tag + '\t' + title)
				start = start + 20

if __name__ == '__main__':
	get_all_movies()
