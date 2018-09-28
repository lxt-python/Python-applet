# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 21:19:22 2018

@author: Administrator
"""

from pyecharts import Map, Geo
import pymysql
"""
# 世界地图数据
value = [95.1, 23.2, 43.3, 66.4, 88.5]
attr= ["China", "Canada", "Brazil", "Russia", "United States"]

# 省和直辖市
province_distribution = {'河南': 45.23, '北京': 37.56, '河北': 21, '辽宁': 12, '江西': 6, '上海': 20, '安徽': 10, '江苏': 16, '湖南': 9, '浙江': 13, '海南': 2, '广东': 22, '湖北': 8, '黑龙江': 11, '澳门': 1, '陕西': 11, '四川': 7, '内蒙古': 3, '重庆': 3, '云南': 6, '贵州': 2, '吉林': 3, '山西': 12, '山东': 11, '福建': 4, '青海': 1, '舵主科技，质量保证': 1, '天津': 1, '其他': 1}
provice=list(province_distribution.keys())
values=list(province_distribution.values())

# 城市 -- 指定省的城市 xx市
city = ['郑州市', '安阳市', '洛阳市', '濮阳市', '南阳市', '开封市', '商丘市', '信阳市', '新乡市']
values2 = [1.07, 3.85, 6.38, 8.21, 2.53, 4.37, 9.38, 4.29, 6.1]

# 区县 -- 具体城市内的区县  xx县
quxian = ['夏邑县', '民权县', '梁园区', '睢阳区', '柘城县', '宁陵县']
values3 = [3, 5, 7, 8, 2, 4]
map0 = Map("世界地图示例", width=1200, height=600)
map0.add("世界地图", attr, value, maptype="world",  is_visualmap=True, visual_text_color='#000')
map0.render(path="./世界地图.html")
# maptype='china' 只显示全国直辖市和省级
# 数据只能是省名和直辖市的名称
map = Map("中国地图",'中国地图', width=1200, height=600)
map.add("", provice, values, visual_range=[0, 50],  maptype='china', is_visualmap=True,
    visual_text_color='#000')
map.show_config()
map.render(path="./中国地图.html")
# 河南地图  数据必须是省内放入城市名
map2 = Map("湖北地图",'湖北', width=1200, height=600)
map2.add('湖北', city, values2, visual_range=[1, 10], maptype='湖北', is_visualmap=True, visual_text_color='#000')
map2.show_config()
map2.render(path="./湖北地图.html")
# # 商丘地图 数据为商丘市下的区县
map3 = Map("武汉地图",'武汉', width=1200, height=600)
map3.add("武汉", quxian, values3, visual_range=[1, 10], maptype='武汉', is_visualmap=True,
    visual_text_color='#000')
map3.render(path="./武汉地图.html")
"""
def show():
    selectsql = "SELECT distr_name,distr_num FROM whdistricts;"
    cur.execute(selectsql.encode('utf-8'))

    house=list(cur.fetchall())
    """
    data = [
    ("海门", 9),("鄂尔多斯", 12),("招远", 12),("舟山", 12),("齐齐哈尔", 14),("盐城", 15),
    ("赤峰", 16),("青岛", 18),("乳山", 18),("金昌", 19),("泉州", 21),("莱西", 21),
    ("日照", 21),("胶南", 22),("南通", 23),("拉萨", 24),("云浮", 24),("梅州", 25)]
    """
    hou=[]
    hou+=house[1:8]+house[9:]
    
    attr = [i[0] for i in hou]
    
    value = [j[1] for j in hou]
    m = max(value)
    for i in range(len(attr)):
        if attr[i][-1]!="区":
            attr[i]+="区"
    # # 商丘地图 数据为商丘市下的区县
    map3 = Map("武汉市房源数量分布图",'武汉', width=1200, height=600)
    map3.add("武汉", attr, value, visual_range=[0, m+1], maptype='武汉', is_visualmap=True,
        visual_text_color='#000')
    map3.render(path="./房源数量热力图.html")



if __name__ == "__main__":
    db = pymysql.connect(
            host="***",       # 数据库主机地址
            user="***",    # 数据库用户名
            passwd="***",   # 数据库密码
            database="***"
            )
    cur = db.cursor()
    show()




