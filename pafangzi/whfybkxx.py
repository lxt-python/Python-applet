# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 10:03:41 2018

@author: Administrator
"""

import pymysql
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import math
import re
from lxml import etree
import requests

DB = "whbk"
base_url = "https://wh.ke.com"
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"}

def get_item_num(entry_url):
    r = requests.get(entry_url, headers=headers, verify=False)
    content = r.content.decode("utf-8")
    root = etree.HTML(content)
    num_nodes = root.xpath('.//div[@class="content "]//h2[contains(@class, "total")]/span')
    if len(num_nodes) == 0:
        raise Exception("no total number for {}".format(entry_url))
    num_str = num_nodes[0].text.strip()
    return int(num_str)

def get_houses_by_sub_district(distr_name,sub_distr_name,entry_url):
    global js
    url_patt = entry_url + "pg{}/"

    total_num = get_item_num(entry_url)
    last_page = math.ceil(total_num/30)
    i = 1
    for i in range(1, last_page+1, 1):
        url = url_patt.format(i)
        r = requests.get(url, verify=False)
        content = r.content.decode("utf-8")
        root = etree.HTML(content)
        content_node = root.find('.//div[@class="content "]')
        if content_node is None:
            print(url)
            r = requests.get(url, verify=False)
            content = r.content.decode("utf-8")
            root = etree.HTML(content)
            ul_node = root.find('.//div[@class="content "]')

        ul_node = root.find('.//ul[@class="sellListContent"]')
        div_info = ul_node.xpath('.//div[contains(@class, "info")]')
        for div_node in div_info:
            title_nodes = div_node.xpath('./div[@class="title"]/a[contains(@class, "maidian-detail")]')
            if len(title_nodes) == 0:
                print("title not found")
                continue
            title_node = title_nodes[0]
            title = title_node.text
            maidian = title_node.attrib["data-maidian"]
            url = title_node.attrib["href"]

            xiaoqu_nodes = div_node.xpath('./div[@class="address"]/div[@class="houseInfo"]/a')
            xiaoqu_name = ""
            house_info = ""
            if len(xiaoqu_nodes) > 0:
                xiaoqu_name = xiaoqu_nodes[0].text
                house_info = xiaoqu_nodes[0].tail

            pos_nodes = div_node.xpath('./div[@class="flood"]/div[@class="positionInfo"]/span')
            building_info = ""
            if len(pos_nodes) > 0:
                building_info = pos_nodes[0].tail
                matched = re.search(r'(.*)\s+-\s+$', building_info)
                if matched:
                    building_info = matched.group(1)

            area_nodes = div_node.xpath('./div[@class="flood"]/div[@class="positionInfo"]/a')
            area = ""
            if len(area_nodes) > 0:
                area_node = area_nodes[0]
                area = area_node.text

            follow_nodes = div_node.xpath('./div[@class="followInfo"]/span')
            follow_info = ""
            if len(follow_nodes) > 0:
                follow_node = follow_nodes[0]
                follow_info = follow_node.tail

            subway_nodes = div_node.xpath('./div[@class="tag"]/span[@class="subway"]')
            subway_info = ""
            if len(subway_nodes) > 0:
                subway_node = subway_nodes[0]
                subway_info = subway_node.text

            tax_nodes = div_node.xpath('./div[@class="tag"]/span[@class="taxfree"]')
            tax_info = ""
            if len(tax_nodes) > 0:
                tax_node = tax_nodes[0]
                tax_info = tax_node.text

            price_nodes = div_node.xpath('./div[@class="priceInfo"]/div[@class="totalPrice"]/span')
            price_num = 0
            price_unit = ""
            if len(price_nodes) > 0:
                price_node = price_nodes[0]
                price_num = price_node.text
                price_unit = price_node.tail

            up_nodes = div_node.xpath('./div[@class="priceInfo"]/div[@class="unitPrice"]')
            unit_price = 0
            if len(up_nodes) > 0:
                up_node = up_nodes[0]
                unit_price = up_node.attrib["data-price"]
            # SQL 有就更新没有就插入
            sql = "REPLACE INTO whfybk (item_id,\
            distr_name,\
            sub_distr_name,\
            title,\
            url,\
            house_info,\
            xiaoqu_name,\
            building_info,\
            area,\
            follow_info,\
            subway_info,\
            tax_info,\
            price_num,\
            price_unit,\
            unit_price) VALUES('%s', '%s', '%s', '%s', '%s',\
                      '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"%(maidian,\
                      distr_name,\
                      sub_distr_name,\
                      title,\
                      url,\
                      house_info,\
                      xiaoqu_name,\
                      building_info,\
                      area,\
                      follow_info,\
                      subway_info,\
                      tax_info,\
                      price_num,\
                      price_unit,\
                      unit_price)
            try:
                # 执行SQL语句
                cursor.execute(sql)
                print(js)
                js+=1
                # 提交修改
                db.commit()
            except:
                # 发生错误时回滚
                print(0)
                db.rollback()
        i += 1

def get_all_houses():
    selectsql = "select * from whsubdistricts"
    cur.execute(selectsql.encode('utf-8'))
    data = cur.fetchall() #所有
    start = 1
    for sub_distr in data:
        entry_url = sub_distr[2]
        distr_name = sub_distr[0]
        sub_distr_name = sub_distr[1]
        #if distr_name == "福田区" and sub_distr_name == "银湖":
        #    start = 1
        if start == 1:
            get_houses_by_sub_district(distr_name,sub_distr_name,entry_url)
            
if __name__ == "__main__":
    global js
    js=1
    db = pymysql.connect(
            host="***",       # 数据库主机地址
            user="***",    # 数据库用户名
            passwd="***",   # 数据库密码
            database="***"
            )
    cur = db.cursor()
    cursor = db.cursor()
    get_all_houses()