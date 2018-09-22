# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 18:09:25 2018

@author: Administrator
"""
from rancolors import randomcolor
from pylab import *
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

import pymysql
import numpy as np
import matplotlib.pyplot as plt

colorss = randomcolor(10,14)

def stats():
    selectsql = "SELECT distr_name,count(*) num FROM whfybeike_copy GROUP BY distr_name;"
    cur.execute(selectsql.encode('utf-8'))
    houses = np.array(cur.fetchall()) #所有
    labels = [lab[0] for lab in houses]
    sum=0
    for lab in houses:
        sum+=int(lab[1])
    sizes = [lab[1] for lab in houses]
    plt.pie(sizes, labels=labels,colors=colorss, autopct='%2.0f%%', shadow=False)
    plt.legend(loc='center left',bbox_to_anchor=(-0.25, -0.15), ncol=7, labels=labels)

    plt.axis('equal')
    plt.title('每个区房源分布')
    plt.show()
    plt.tight_layout()
    

    
if __name__ == "__main__":
    db = pymysql.connect(
            host="***",       # 数据库主机地址
            user="***",    # 数据库用户名
            passwd="***",   # 数据库密码
            database="***"
            )
    cur = db.cursor()
    stats()