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
# 使用proxy传入外部ip
proxy = {
    'http':'218.1.200.211:57114',
    'http':'112.14.47.6:52024',
    'http':'123.182.59.3:8089',
    'http':'27.46.52.126:9797',
    'http':'182.139.111.204:9000'
}

the_url = f'https://www.bilibili.com/v/popular/rank/bangumi/'
the_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54'}

resp = requests.get(url=the_url, headers=the_headers, proxies=proxy)
random_sleep()
data = resp.content.decode('UTF-8')
soup = BeautifulSoup(data, 'lxml')

# 获取番剧的名字
bangumi_names_list = []
names = soup.find_all(class_='title')
for name in names:
    bangumi_names_list.append(name.get_text('title'))
# 获取番剧的点赞量 Number of likes下面简称nol
bangumi_play_list = []
bangumi_nols_list = []
package = soup.find_all(class_='data-box')
for j in range(1, len(package), 3):
    the_play = re.search(r'[0-9].*', package[j].get_text())
    bangumi_play_list.append(the_play.group())
for i in range(2, len(package), 3):
    the_point = re.search(r'[0-9].*[\u4e00-\u9fa5]', package[i].get_text())
    bangumi_nols_list.append(the_point.group())
resp.close()

conn = pymysql.connect(
    host='localhost',
    port=3306,
    database='bzhantop50',
    user='zkr',
    password='123456',
    charset='utf8'
)
cur = conn.cursor()
sql1 = 'CREATE TABLE top50(番名 varchar(50), 播放量 varchar(40),点赞量 varchar(40))'
cur.execute(sql1)
cur.close()
for i in range(len(bangumi_names_list)):
    cur1 = conn.cursor()
    sql = 'INSERT INTO top50 VALUES(%s, %s, %s)' % (buildValue(bangumi_names_list[i]), buildValue(bangumi_play_list[i]), buildValue(bangumi_nols_list[i]))
    cur1.execute(sql)
    conn.commit()
    cur1.close()
conn.close()