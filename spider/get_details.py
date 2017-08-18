#!python3

'''
根据电影id获取详细信息

author: justZero
email: alonezero@foxmail.com
date: 2017-8-7
'''

import re
import time
import requests
from bs4 import BeautifulSoup
from logger import Logger
from constant import HEADERS


logger = Logger('Spider_get_details', 'spider.log')

def get_movie_detail(url):
	r = requests.get(url, headers=HEADERS)
	r.raise_for_status()
	r.encoding = 'utf-8'

	html = BeautifulSoup(r.text, 'html.parser')
	info = html.select('#info')[0].get_text()

	director  = extract('导演', info)
	composer  = extract('编剧', info)
	actor     = extract('主演', info)
	category  = extract('类型', info)
	district  = extract('制片国家/地区', info)
	language  = extract('语言', info)
	showtime  = extract('上映日期', info)
	length    = extract('片长', info)
	othername = extract('又名', info)

	description = html.find_all("span", attrs={"property": "v:summary"})
	description = description[0].get_text().strip().replace('\n','\t') if len(description) > 0 else '无'

	return [director, composer, actor, category, district, language, showtime, length, othername, description]
		

def get_all_movie_details(start=1, append=False):
	count = 1 # 电影详情抓取成功数

	inputFile = 'data/douban_movie.txt'
	outputFile = 'data/douban_movie_detail.txt'

	store_mode = 'a' if append else 'w'
	with open(inputFile, 'r', encoding='utf8') as fr:
		with open(outputFile, store_mode, encoding='utf8') as fw:
			# 先读取第一行，过滤掉 csv 标题行
			title_line = fr.readline()

			if start == 1:
				fw.write('id^title^url^cover^rate^director^composer^actor^category^district^language^showtime^length^othername^description\n')

			# 断点续爬：读取到目标起始行再继续爬取
			for i in range(1, start):
				temp = fr.readline()
				count = count + 1

			for line in fr:
				simple_info = line.strip().split(';')
				movieId, title, url, cover, rate = simple_info

				try:
					detail_info = get_movie_detail(url)
				except Exception as e:
					logger.exception(str(count)+'《'+title+'》详细信息抓取失败，URL: '+url)
					exit()
				else:
					record = '^'.join( simple_info+detail_info ) + '\n'
					fw.write(record)
					time.sleep(4) # 设置延迟，避免IO阻塞
					logger.info(str(count)+"\t"+title)
					count = count + 1

			logger.info("电影详细信息爬取数量："+str(count))

# 根据关键字提取字符串信息
def extract(keyword, str):
	pattern = '\\n'+keyword+':(.+?)\\n'
	value = re.findall(pattern, str)
	return value[0].strip() if len(value) > 0 else '未知'

if __name__ == '__main__':
	# get_movie_detail('https://movie.douban.com/subject/26577541/')
	# get_movie_detail('https://movie.douban.com/subject/26887890/')
	# get_all_movie_details()
	# get_all_movie_details(start=506, append=True)
	# get_all_movie_details(start=2159, append=True)
	get_all_movie_details(start=4006, append=True)
