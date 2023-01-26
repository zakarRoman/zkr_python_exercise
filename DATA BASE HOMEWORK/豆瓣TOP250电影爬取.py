# 部门:人工智能
# 编写人:张开然
# 开发日期: 2023/1/3
# !/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import random
import requests
import openpyxl
from bs4 import BeautifulSoup
import re
import openpyxl.styles
import os
import pymysql
# 先定义一个用来随机休眠的函数
def random_sleep(mu=1, sigma=0.4):
    secs = random.normalvariate(mu, sigma)
    if secs <= 0:
        secs = mu
    time.sleep(secs)

def buildValue(value):
    return '"' + value + '"'

# count是后面访问的参数
count = 0
# 定义出用来存放250个名字，别名，导演，主演，得分，引言的空白列表
names = []
aliases = []
directors = []
actors = []
scores = []
quotes = []
# 所有图片的下载地址的列表
movie_images_download_list = []
movie_images_names_download_list = []
# 使用proxy传入外部ip
proxy = {
    'http':'218.1.200.211:57114',
    'http':'112.14.47.6:52024',
    'http':'123.182.59.3:8089',
    'http':'27.46.52.126:9797',
    'http':'182.139.111.204:9000'
}
# 访问使用的headers,url
the_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54'}
the_url = f'https://movie.douban.com/top250'
# 由于要爬250个电影的信息，所以设置count，每爬完一页加50
while (count<250):
    # 每次输入的参数都是count
    param = {
        "start": count,
        "filter": ""
    }
    # 记得要传proxies
    resp = requests.get(url=the_url, headers=the_headers, params=param, proxies=proxy)
    # 设置随机休眠
    random_sleep()

    data = resp.content.decode('UTF-8')
    soup = BeautifulSoup(data, 'lxml')

    # 获取名字列表
    movie_names_list = soup.find_all('span', attrs={'class': 'title'})
    for name in movie_names_list:
        the_name = re.search(r'<span class="title">(?P<change1>[——?\d?\u4e00-\u9fa5].*?)</span>', str(name))
        if the_name is not None:
            names.append(the_name.group('change1'))
        else: continue

    # 获取别名列表
    movie_alias_list = soup.find_all('span', attrs={'class': 'other'})
    for alias in movie_alias_list:
        the_alias = re.search(r'(<span class="other">(?P<change2>.*?)</span>)', str(alias))
        if the_alias is not None:
            aliases.append(the_alias.group('change2').replace(u'\xa0', ''))
        else:
            aliases.append('无')
            continue

    count += 25# count加25

    # 获取引言列表
    movie_quotes_list = []
    movie_quotes_list_0 = re.finditer(r'(?<=<span>)[0-9]*人评价[\s\S]*?(?=</li>)', str(soup))
    for i in movie_quotes_list_0:
        movie_quotes_list.append(i.group())

    for quote in movie_quotes_list:
        the_quote = re.search(r'(?P<change3>(?<=<span class="inq">).*(?=</span>))', str(quote))
        if the_quote is not None:
            quotes.append(the_quote.group('change3'))
        else:
            quotes.append('无')
            continue
    # 获取导演列表
    informations = soup.find_all('p', attrs={'class': ''})
    for director in informations:
        the_director = re.search(r'导演:\s(?P<change4>.*?)\s', director.get_text())
        if the_director is not None:
            directors.append(the_director.group("change4"))
    # 获取演员列表
    for actor in informations:
        the_actor = re.search(r'主演:\s(?P<change5>.*?)\s', actor.get_text())
        if the_actor is not None:
            actors.append(the_actor.group("change5"))
        else:
            actors.append('无')
            continue

    # 获取得分列表
    span_score = soup.find_all('span', attrs={'class': 'rating_num'})
    for score in span_score:
        the_score = re.search(r'(?P<change6>\d.\d)', str(score))
        if the_score is not None:
            scores.append(the_score.group('change6'))
        else:
            continue

    # 获取封面下载地址列表

    movie_images_download_list_0 = re.finditer(r'(?<= src=").*(?=" width="100"/>)', str(soup))
    for i in movie_images_download_list_0:
        movie_images_download_list.append(i.group())

    movie_images_names_download_list_0 = re.finditer(r'(?<=<img alt=").*(?=" class="")', str(soup))
    for a in movie_images_names_download_list_0:
        movie_images_names_download_list.append(a.group())


resp.close()
conn = pymysql.connect(
    host='localhost',
    port=3306,
    database='doubanmovies',
    user='zkr',
    password='123456',
    charset='utf8'
)
cur = conn.cursor()
sql1 = 'CREATE TABLE top250(影片名 varchar(50),影片别名 varchar(150),导演 varchar(30),主演 varchar(30),评分 varchar(10),引言 varchar(300));'
cur.execute(sql1)
cur.close()
for i in range(len(names)):
    cur1 = conn.cursor()
    sql = 'INSERT INTO top250 VALUES (%s,%s,%s,%s,%s,%s)' % (buildValue(names[i]), buildValue(aliases[i]), buildValue(directors[i]), buildValue(actors[i]), buildValue(str(scores[i])), buildValue(quotes[i]))
    cur1.execute(sql)
    conn.commit()
    cur1.close()
conn.close()
