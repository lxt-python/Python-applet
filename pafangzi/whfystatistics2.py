# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 09:15:31 2018

@author: Administrator
"""

from rancolors import randomcolor
import matplotlib.pyplot as plt
import squarify

#中文及负号处理办法
plt.rcParams['font.sans-serif'] = 'Microsoft YaHei'
plt.rcParams['axes.unicode_minus'] = False
import pymysql
import numpy as np

colorss = randomcolor(10,14)

def shumap():
    selectsql = "SELECT distr_name,aver_unit_price FROM whdistricts;"
    cur.execute(selectsql.encode('utf-8'))
    houses = np.array(cur.fetchall()) #所有
    labels = [lab[0] for lab in houses]
    sizes = [float(lab[1]) for lab in houses]
    labsizes = [lab[1] for lab in houses]
    plot = squarify.plot(sizes, # 指定绘图数据
                     label = labels, # 指定标签
                     color = colorss, # 指定自定义颜色
                     alpha = 0.6, # 指定透明度
                     value = labsizes, # 添加数值标签
                     edgecolor = 'white', # 设置边界框为白色
                     linewidth =3 # 设置边框宽度为3
                    )
    # 设置标签大小为10
    plt.rc('font', size=10)
    # 设置标题大小
    plot.set_title('武汉各区房源均价(元/平米)',fontdict = {'fontsize':15})
    # 除坐标轴
    plt.axis('off')
    # 除上边框和右边框刻度
    plt.tick_params(top = 'off', right = 'off')
    plt.savefig('./whfyjj.png')
    # 图形展示
    plt.show()
     
    

if __name__ == "__main__":
    db = pymysql.connect(
            host="***",       # 数据库主机地址
            user="***",    # 数据库用户名
            passwd="***",   # 数据库密码
            database="***"
            )
    cur = db.cursor()
    shumap()