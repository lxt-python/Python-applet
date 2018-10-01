# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 19:10:20 2018

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 09:53:28 2018

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
    d = pd.read_excel("./one_hot.xlsx", sheetname=None)
    print(d)

    

    
if __name__ == "__main__":
    
    show()