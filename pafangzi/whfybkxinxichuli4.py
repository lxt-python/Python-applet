# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 19:10:20 2018

@author: Administrator
"""

import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from random import sample
from sklearn import preprocessing
from scipy.spatial.distance import cdist
from sklearn.decomposition import PCA
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

def k_means_cluster(points,k,first_centroids=None, predict_method=None):
    max_iters=1000
    N, D = points.shape
    K=k      # 被聚为K类
    # 初始聚类中心……
    centroids = tf.Variable(points[sample(range(N), K)] if first_centroids is None else first_centroids)
    # 样本归属聚类中心……
    cluster_assignments = tf.Variable(tf.zeros([N], dtype=tf.int64))
    # 同时计算所有样本与聚类中心的距离……
    rep_points = tf.reshape(tf.tile(points, [1, K]), [N, K, D])
    rep_centroids = tf.reshape(tf.tile(centroids, [N, 1]), [N, K, D])
    sum_squares = tf.reduce_sum(tf.square(rep_points - rep_centroids), reduction_indices=2)

    # 样本对应的聚类中心索引……
    best_centroids = tf.argmin(sum_squares, 1)
    # 新聚类中心对应的样本索引……
    centroids_indies = tf.argmin(sum_squares, 0)

    # 按照`best_centroids`中相同的索引，将points求和……
    total = tf.unsorted_segment_sum(points, best_centroids, K)
    # 按照`best_centroids`中相同的索引，将points计数……
    count = tf.unsorted_segment_sum(tf.ones_like(points), best_centroids, K)
    # 以均值作为新聚类中心的值……
    means = total / count

    did_assignments_change = tf.reduce_any(tf.not_equal(best_centroids, cluster_assignments))

    with tf.control_dependencies([did_assignments_change]):
        do_updates = tf.group(centroids.assign(means), cluster_assignments.assign(best_centroids))
    init = tf.initialize_all_variables()

    sess = tf.Session()
    sess.run(init)

    iters, changed = 0, True
    while changed and iters < max_iters:
        iters += 1
        [changed, _] = sess.run([did_assignments_change, do_updates])

    [centers, cindies, assignments] = sess.run([centroids, centroids_indies, cluster_assignments])
    print(k,iters)
    return iters, centers, assignments


def show(d,m):
    #以下是将聚类结果可视化出来
    #PCA(n_components=2)表示将4个特征的向量降维到二维，即可以画在平面
    pca_model = PCA(n_components=2)
    #将iris.data转换成标准形式，然后存入reduced_data中
    reduced_data = pca_model.fit_transform(d)
    #将前面的几何中心点centers也转换成标准形式，然后存入reduced_centers中
    #reduced_centers = pca_model.transform(centers)
    ans=[]
    for k in range(1,m):
        iters, centers, assignments = k_means_cluster(reduced_data, k)
        test_acc = sum(np.min(cdist(reduced_data, centers, metric='euclidean'), axis=1))/ d.shape[0]
        ans.append(test_acc)
    x=[i for i in range(1,m)]
    plt.figure() 
    plt.plot(x,ans,'o-')
    plt.savefig('./whfyjl.png')
    plt.show()

    

    
if __name__ == "__main__":
    d = pd.read_excel("./one_hot.xlsx", sheetname='123')
    d = np.array(d)
    scaler = preprocessing.StandardScaler().fit(d)
    data = scaler.transform(d)
    print(data)
    show(data,30)