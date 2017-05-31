#!/usr/bin/python
# coding: UTF-8

'''
指定日のプロットを行う
累積和、移動平均つき

python plot_day.py xxxx.dump 20120101
'''

import collections
import sys
import numpy as np
import matplotlib.pyplot as plt
import pybursts
import datetime
import matplotlib.dates as mdates
import pickle
import search_burst as sb

co_prob_df = sb.open_dump('rplinear/rp_co_prob_df')
co_edge_df = sb.open_dump('rplinear/rp_edge_co_df')

xj = co_prob_df['x']
yj = co_prob_df['y_jaccard'] * (10 ** 5 )
xs = co_prob_df['x']
ys = co_prob_df['y_simpson'] * (10 ** 5 )
xej = co_edge_df['x']
yej = co_edge_df['y_jaccard'] * (10 ** 5 )
xes = co_edge_df['x']
yes = co_edge_df['y_simpson'] * (10 ** 5 )

for i in [0,1]:
    kind = ['jaccard','simpson'][i]

    fig = plt.figure(figsize=(10,6))
    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.95, bottom=0.15, left=0.15)

    y = [yj,ys][i]
    x = [xj,xs][i]

    plt.scatter(x,y, marker='.', c=None, color='gray', label='no causality')

    # edge plot
    y = [yej,yes][i]
    x = [xej,xes][i]

    plt.scatter(x,y, marker='o', c=None, color='red', label='causality')

    plt.yscale("log")

    plt.xticks(fontsize='18')
    plt.yticks([10 ** i for i in range(1,6)],
               ['$1.0^{-4}$','$1.0^{-3}$','$1.0^{-2}$','$1.0^{-1}$','1.0'],
               fontsize='25')

    plt.ylim(1., 10. ** 5 + 10 ** 4)
    plt.grid()

    plt.xlabel(r'$|A \cup B|$', fontsize='23')
    ax.xaxis.set_label_coords(0.5, -0.13)
    if i==0:
        ax.set_ylabel(r'$J(A,B)$', fontsize='23')
    else:
        ax.set_ylabel(r'$S(A,B)$', fontsize='23')

    ax.yaxis.set_label_coords(-0.15, 0.5)
    plt.legend(prop={'size':20},loc='lower left')
    plt.savefig('{0}_edge.png'.format(kind))
    #plt.savefig('{0}_edge.eps'.format(kind))
