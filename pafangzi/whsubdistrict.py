# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 21:40:54 2018

@author: Administrator
"""

import pymysql
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import math
import re
from lxml import etree
import time
import json
import requests

DB = "whbk"
base_url = "https://wh.ke.com"

def get_sub_districts():
    result=[]
    districts = data
    for item in districts:
        distr_name = item[0]
        distr_url = item[1]
        r = requests.get(distr_url, verify=False)
        content = r.content.decode("utf-8")
        root = etree.HTML(content)
        subdistr_nodes = root.xpath('.//div[@class="m-filter"]//div[@data-role="ershoufang"]/div')[1].xpath('./a')
        for node in subdistr_nodes:
            sub_distr_name = node.text
            sub_distr_url = base_url + node.attrib["href"]
            result.append([distr_name,sub_distr_name,sub_distr_url])
    return result

if __name__ == "__main__":
    db = pymysql.connect(
            host="localhost",       # 数据库主机地址
            user="asx",    # 数据库用户名
            passwd="xbd",   # 数据库密码
            database="whbk"
            )
    cur = db.cursor()
    selectsql = "select * from whdistricts"
    cur.execute(selectsql.encode('utf-8'))
    data = cur.fetchall() #所有
    disc=get_sub_districts()
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
     
    # SQL 有就更新没有就插入
    for i in range(len(disc)):
        sql = "REPLACE INTO whsubdistricts (district,sub_district,url) VALUES('%s', '%s', '%s')"%(disc[i][0],disc[i][1],disc[i][2])
        try:
           # 执行SQL语句
           cursor.execute(sql)
           # 提交修改
           db.commit()
        except:
           # 发生错误时回滚
           db.rollback()
    db.close()