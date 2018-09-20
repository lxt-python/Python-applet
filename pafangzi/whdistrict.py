# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 17:10:12 2018

@author: Administrator
"""

import pymysql
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import re
from lxml import etree
import requests

DB = "whbk"
base_url = "https://wh.ke.com"

def get_districts():
    url = base_url + "/ershoufang/"
    r = requests.get(url, verify=False)
    content = r.content.decode("utf-8")
    root = etree.HTML(content)
    distr_nodes = root.xpath('.//div[@class="m-filter"]//div[@data-role="ershoufang"]/div/a')
    result = []
    for node in distr_nodes:
        rel_url = node.attrib["href"]
        distr_url = ""
        if re.match(r'https://', rel_url):
            distr_url = rel_url
        else:
            distr_url = base_url + rel_url
        distr_name = node.text
        result.append([distr_name, distr_url])
        
    
    return result
if __name__ == "__main__":
    db = pymysql.connect(
            host="***",       # 数据库主机地址
            user="***",    # 数据库用户名
            passwd="***",   # 数据库密码
            database=DB
            )
    disc=get_districts()
    print(disc)
    # 关闭连接
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
     
    # SQL 有就更新没有就插入
    for i in range(len(disc)):
        sql = "REPLACE INTO whdistricts (distr_name,distr_url) VALUES('%s', '%s')"%(disc[i][0],disc[i][1])
        try:
           # 执行SQL语句
           cursor.execute(sql)
           # 提交修改
           db.commit()
        except:
           # 发生错误时回滚
           db.rollback()
     
    # 关闭连接
    db.close()