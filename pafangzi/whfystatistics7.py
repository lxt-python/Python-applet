# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 14:03:13 2018

@author: Administrator
"""
import pymysql
import sqlalchemy
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pylab import *
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号


def show():
    sql1 = "SELECT unit_price FROM whfybk;"
    data = pd.read_sql(sql1,db) 
    #print(data)
    ans={}
    ans1=[4000+i*2000 for i in range(39)]
    
    for i in range(len(ans1)-1):
        ans[ans1[i]]=[i,0]
    for i in data["unit_price"]:
        a=int(i/2000)
        ans[a*2000][1]+=1
    
    ans2=pd.DataFrame(sorted(ans.items(),key=lambda x:x[1][0]))
    ans3=[]
    ans4=[]
    for i in range(ans2.shape[0]):
        ans3.append(ans2[0][i])
    for i in range(ans2.shape[0]):
        ans4.append(ans2[1][i][1])    
        
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    width=1
    x_bar=np.arange(38)
    rect=ax.bar(left=x_bar,height=ans4,width=width,color='#007000')
                
    for rec in rect:
        x=rec.get_x()
        height=rec.get_height()
        ax.text(x+0.1,1.02*height,str(height),rotation=90)
 
 
    ax.set_xticks(x_bar)
    ax.set_xticklabels(ans3,rotation=90)
    ax.set_ylabel("mid_aver_unit_price")
    ax.set_title("武汉房源均价数量条形图")
    #ax.grid(True)
    #plt.savefig('./whfyjjsl.png')
    #plt.show()
    plt.plot(ans4,color='r')
    #填充颜色
    plt.savefig('./whfyjjsl.png')
    plt.show()
    #通过高斯拟合添加置信区间

    

    
if __name__ == "__main__":
    db = pymysql.connect(
            host="***",       # 数据库主机地址
            user="***",    # 数据库用户名
            passwd="***",   # 数据库密码
            database="***"
            )
    cur = db.cursor()
    show()
