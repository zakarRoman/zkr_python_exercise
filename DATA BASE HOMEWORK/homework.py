# 部门:人工智能
# 编写人:张开然
# 开发日期: 2023/1/2
# !/usr/bin/python
# -*- coding: UTF-8 -*-
import pymysql
list_hero = ['美国队长', '钢铁侠', '雷神', '绿巨人', '鹰眼', '黑寡妇']
power_list = ['superman', 'money', 'thunder', 'power', 'bowman', 'excellent']
gender_list = ['男', '男', '男', '男', '男', '女']
score_list = [1.5, 2.3, 2.2, 5.6, 2.3, 8.9]
def buildValue(value):
    return '"' + value + '"'


conn = pymysql.connect(
    host='localhost',
    port=3306,
    database='homework',
    user='zkr',
    password='123456',
    charset='utf8'
)
cur = conn.cursor()
# sql1 = 'CREATE TABLE test1(影片名 varchar(50),影片别名 varchar(150),导演 varchar(30),主演 varchar(30),评分 varchar(10),引言 varchar(300));'
# sql2 = 'CREATE TABLE HEROS(name varchar(30),power varchar(30),gender varchar(30),score decimal(3,2))'
for i in range(0, len(list_hero)):
    cur = conn.cursor()
    sql = 'INSERT INTO heros VALUES (%s, %s, %s,%s)' % (buildValue(list_hero[i]), buildValue(power_list[i]), buildValue(gender_list[i]), buildValue(str(score_list[i])))
    cur.execute(sql)
    conn.commit()
    cur.close()
# cur.execute(sql2)
cur.close()
conn.close()

