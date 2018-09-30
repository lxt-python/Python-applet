# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 22:11:12 2018

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 14:03:13 2018

@author: Administrator
"""
import pymysql
import sqlalchemy
import pandas as pd
import numpy as np

def show():
    sql1="select *from (select xiaoqu_name from whfybk WHERE build_year=0)as a GROUP BY xiaoqu_name;"
    cur.execute(sql1.encode('utf-8'))
    db.commit() #提交到数据库执行
    xiaoqu_name=np.array(cur.fetchall())
    print(xiaoqu_name.shape)
    xiaoqu_names=[]
    for i in range(xiaoqu_name.shape[0]):
        xiaoqu_names.append(xiaoqu_name[i][0])
    print(xiaoqu_names)
    for i in xiaoqu_names:
        sql2="UPDATE whfybk \
                SET build_year = (\
                	SELECT\
                		build_year\
                	FROM\
                		( SELECT build_year, count( * ) num \
                        FROM ( SELECT * FROM whfybk WHERE xiaoqu_name = '%s' AND build_year !=0) AS a \
                        GROUP BY build_year ) AS b GROUP BY\
                		build_year\
                	ORDER BY\
                		num DESC \
                		LIMIT 1 \
                	) \
                WHERE\
                	xiaoqu_name = '%s'\
                and build_year=0;"% (i, i)
        cur.execute(sql2.encode('utf-8'))
        db.commit() #提交到数据库执行
    
    """
    sql1 = "SELECT * FROM test1;"
    data = pd.read_sql(sql1,db) 
    print(data.columns)
    """
    
if __name__ == "__main__":
    db = pymysql.connect(
            host="***",       # 数据库主机地址
            user="***",    # 数据库用户名
            passwd="***",   # 数据库密码
            database="***"
            )
    cur = db.cursor()
    show()
