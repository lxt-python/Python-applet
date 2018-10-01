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
from scipy.spatial.distance import cdist

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

def k_means_cluster(points,k,first_centroids=None, predict_method=None):
    max_iters=100
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
    return iters, centers, assignments


def show(d,m):
    ans=[]
    for k in range(1,m):
        iters, centers, assignments = k_means_cluster(d, k)
        test_acc = sum(np.min(cdist(d, centers, metric='euclidean'), axis=1))/ d.shape[0]
        ans.append(test_acc)
    x=[i for i in range(1,m)]
    plt.figure() 
    plt.plot(x,ans,'o-')
    plt.show()

    

    
if __name__ == "__main__":
    d = pd.read_excel("./one_hot.xlsx", sheetname=None)
    data = np.array(d['123'])
    show(data,20)