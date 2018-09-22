# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 14:35:57 2018

@author: Administrator
"""
import pymysql
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import re

def parse_house_info(house_info):
    items = house_info.split("|")
    house_type = "apartment"
    matched = re.search(r'别墅', items[1])
    info_items = items[1:]
    if matched:
        info_items = items[2:]
        house_type = "house"

    if len(info_items) < 4:
        print(house_info)
        return ["", -1, -1, -1, -1, "", ""]
    room_info = info_items[0]
    size_info = info_items[1]
    direc_info = info_items[2]
    decor_info = info_items[3]
    lift_info = ""
    if len(info_items) >= 5:
        lift_info = info_items[4]
    matched = re.search(r'(\d+)室(\d+)厅', room_info)
    shi_num = 0
    ting_num = 0
    if matched:
        shi_num = int(matched.group(1))
        ting_num = int(matched.group(2))

    matched = re.search(r'([.0-9]+)平米', size_info)
    size = 0.0
    if matched:
        size = float(matched.group(1))

    has_lift = None
    if re.search(r'有电梯', lift_info):
        has_lift = True
    elif re.search(r'无电梯', lift_info):
        has_lift = False
    result = [house_type, shi_num, ting_num, size, has_lift, direc_info, decor_info]
    return result


def update_house_info():
    selectsql = "select * from whfybeike_copy2"
    cur.execute(selectsql.encode('utf-8'))
    houses = cur.fetchall() #所有
    for house in houses:
        object_id = house[0]
        price_num = float(house[12])
        unit_price = float(house[14])
        building_info = house[7]
        matched = re.search(r'(\d+)年', building_info)
        build_year = 0
        if matched:
            build_year = int(matched.group(1))
        sql = "update whfybeike_copy2 set price_num = '%.f',unit_price = '%.f',build_year = '%d' Where item_id='%s';" % (price_num, unit_price, build_year,object_id)
        try:
            cur.execute(sql) #执行sql语句
            db.commit() #提交到数据库执行
        except:
            db.rollback() #发生错误后回滚
        info = parse_house_info(house[5])
        sql = "update whfybeike_copy2 set house_type ='%s', shi_num='%d', ting_num='%d', size='%.2f', has_lift='%s', direction='%s', decoration='%s' Where item_id='%s';" % (info[0],info[1],info[2],info[3],info[4],info[5],info[6],object_id)
        try:
            cur.execute(sql) #执行sql语句
            db.commit() #提交到数据库执行
        except:
            db.rollback() #发生错误后回滚


if __name__ == "__main__":
    db = pymysql.connect(
            host="***",       # 数据库主机地址
            user="***",    # 数据库用户名
            passwd="***",   # 数据库密码
            database="***"
            )
    cur = db.cursor()
    update_house_info()