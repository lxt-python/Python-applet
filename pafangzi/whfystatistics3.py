# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 09:15:43 2018

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 18:09:25 2018

@author: Administrator
"""
from rancolors import randomcolor
from pylab import *
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

import numpy as np
import pymysql
import matplotlib.pyplot as plt

colorss = randomcolor(10,14)

def stamap():
    selectsql = "SELECT distr_name,distr_num,aver_unit_price FROM whdistricts;"
    cur.execute(selectsql.encode('utf-8'))

    house=list(cur.fetchall())
    for t in house:
        house[house.index(t)]=list(t)
    house1 = sorted(house,key=lambda x:x[1],reverse=True)
    house2 = sorted(house,key=lambda x:x[2],reverse=True)
    labels1 = [lab[0] for lab in house1]
    sizes1 = [lab[1] for lab in house1]
    labels2 = [lab[0] for lab in house2]
    sizes2 = [lab[2] for lab in house2]
    
    
    
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    width=1
    x_bar=np.arange(14)
    rect=ax.bar(left=x_bar,height=sizes2,width=width,color=colorss)
    for rec in rect:
        x=rec.get_x()
        height=rec.get_height()
        ax.text(x+0.1,1.02*height,str(height),rotation=60)
 
 
    ax.set_xticks(x_bar)
    ax.set_xticklabels(labels2,rotation=60)
    ax.set_ylabel("aver_unit_price")
    ax.set_title("武汉房源均价条形图")
    ax.grid(True)
    plt.savefig('./whfyjj3.png')
    plt.show()


    

    
if __name__ == "__main__":
    db = pymysql.connect(
            host="***",       # 数据库主机地址
            user="***",   # 数据库用户名
            passwd="***",   # 数据库密码
            database="***"
            )
    cur = db.cursor()
    stamap()