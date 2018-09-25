# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 10:47:12 2018

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
    selectsql = "SELECT distr_name, unit_price FROM whfybk;"
    cur.execute(selectsql.encode('utf-8'))

    house=list(cur.fetchall())
    hou={}
    hous=[]
    for t in house:
        if t[0] in hou:
            hou[t[0]].append(t[1])
        else:
            hou[t[0]]=[]
            hou[t[0]].append(t[1])
    for key,value in hou.items():
        value.sort()
        t=len(value)//2-1
        hous.append([key,value[t]])


    house1 = sorted(hous,key=lambda x:x[1],reverse=True)
    labels1 = [lab[0] for lab in house1]
    sizes1 = [lab[1] for lab in house1]
    print(sizes1)
    
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    width=1
    x_bar=np.arange(12)
    rect=ax.bar(left=x_bar,height=sizes1,width=width,color=colorss)
    for rec in rect:
        x=rec.get_x()
        height=rec.get_height()
        ax.text(x+0.1,1.02*height,str(height),rotation=60)
 
 
    ax.set_xticks(x_bar)
    ax.set_xticklabels(labels1,rotation=60)
    ax.set_ylabel("mid_aver_unit_price")
    ax.set_title("武汉房源均价中位数条形图")
    ax.grid(True)
    plt.savefig('./whfyjjz.png')
    plt.show()

  
if __name__ == "__main__":
    db = pymysql.connect(
            host="***",       # 数据库主机地址
            user="***",    # 数据库用户名
            passwd="***",   # 数据库密码
            database="***"
            )
    cur = db.cursor()
    stamap()