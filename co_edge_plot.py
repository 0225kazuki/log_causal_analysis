#!/usr/bin/python
# coding: UTF-8

'''
coburst, edgeプロット
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

co_prob_df = sb.open_dump('co_prob_df')
co_edge_df = sb.open_dump('rp_edge_coburst')

xj = co_prob_df['x']
yj = co_prob_df['y_jaccard'] * (10 ** 5 )
xs = co_prob_df['x']
ys = co_prob_df['y_simpson'] * (10 ** 5 )
xej = co_edge_df['x']
yej = co_edge_df['y_jaccard'] * (10 ** 5 )
xes = co_edge_df['x']
yes = co_edge_df['y_simpson'] * (10 ** 5 )

df_bool = [False]*co_prob_df.shape[0]
for i in [x for x in co_prob_df['EvPair'] if (x[0][:3]=='10_' or x[1][:3]=='11_') or (x[0][:3]=='11_' or x[1][:3]=='10_')]:
    df_bool |= co_prob_df['EvPair']==i
x1 = co_prob_df[df_bool]['x']
y1j = co_prob_df[df_bool]['y_jaccard'] * (10 ** 5 )
y1s = co_prob_df[df_bool]['y_simpson'] * (10 ** 5 )

for i in [0,1]:
    kind = ['jaccard','simpson'][i]

    fig = plt.figure(figsize=(10,6))
    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.95, bottom=0.15, left=0.15, right=0.9)

    y = [yj,ys][i]
    x = [xj,xs][i]

    plt.scatter(x,y, marker='.', c=None, color='gray', label='no causality')

    y = [y1j,y1s][i]
    x = x1

    # plt.scatter(x,y, marker='.', c=None, color='blue', label='"Show interface" command')


    # edge plot
    y = [yej,yes][i]
    x = [xej,xes][i]

    plt.scatter(x,y, marker='o', c=None, color='red', label='causality')

    plt.yscale("log")

    plt.xticks(fontsize='18')
    plt.yticks([10 ** i for i in range(1,6)],
               ['$10^{-4}$','$10^{-3}$','$10^{-2}$','$10^{-1}$','1.0'],
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
    # plt.savefig('{0}_edge.png'.format(kind))
    plt.savefig('{0}_edge.eps'.format(kind))

xj = co_prob_df['x']
yj = co_prob_df['y_jaccard']
xs = co_prob_df['x']
ys = co_prob_df['y_simpson']
xej = co_edge_df['x']
yej = co_edge_df['y_jaccard']
xes = co_edge_df['x']
yes = co_edge_df['y_simpson']

df_bool = [False]*co_prob_df.shape[0]
for i in [x for x in co_prob_df['EvPair'] if (x[0][:3]=='10_' and x[1][:3]=='11_') or (x[0][:3]=='11_' and x[1][:3]=='10_')]:
    df_bool |= co_prob_df['EvPair']==i
x1 = co_prob_df[df_bool]['x']
y1j = co_prob_df[df_bool]['y_jaccard']
y1s = co_prob_df[df_bool]['y_simpson']

df_bool = [False]*co_prob_df.shape[0]
for i in [x for x in co_prob_df['EvPair'] if (x[0][:4]=='176_' and x[1][:4]=='401_') or (x[0][:4]=='401_' and x[1][:4]=='176_')]:
    df_bool |= co_prob_df['EvPair']==i
x2 = co_prob_df[df_bool]['x']
y2j = co_prob_df[df_bool]['y_jaccard']
y2s = co_prob_df[df_bool]['y_simpson']

df_bool = [False]*co_prob_df.shape[0]
for i in [x for x in co_prob_df['EvPair'] if (x[0][:4]=='135_' or x[1][:4]=='376_') or (x[0][:4]=='376_' or x[1][:4]=='135_')]:
    df_bool |= co_prob_df['EvPair']==i
x3 = co_prob_df[df_bool]['x']
y3j = co_prob_df[df_bool]['y_jaccard']
y3s = co_prob_df[df_bool]['y_simpson']


for i in [0,1]:
    kind = ['jaccard','simpson'][i]

    fig = plt.figure(figsize=(10,6))
    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.95, bottom=0.15, left=0.15, right=0.9)

    # edge plot
    y = [yej,yes][i]
    x = [xej,xes][i]
    plt.scatter(x,y, marker='o', c=None, color='red', label='causality')


    y = [yj,ys][i]
    x = [xj,xs][i]
    plt.scatter(x,y, marker='.', c=None, color='gray', label='no causality')

    y1=[y1j,y1s][i]
    y2=[y2j,y2s][i]
    y3=[y3j,y3s][i]
    plt.scatter(x1,y1, marker='.', c=None, color='blue', label='"show interface" cmd')
    plt.scatter(x2,y2, marker='.', c=None, color='green', label='"MPLS path/bypath up"')
    plt.scatter(x3,y3, marker='.', c=None, color='orange', label='"MPLS path/bypath down"')

    plt.yticks(fontsize='25')
    plt.xticks(fontsize='18')
    # plt.yticks([i*0.1 for i in range(10)])

    # plt.ylim(0.1,1.02)
    plt.xlim(0,100)
    plt.grid()

    plt.xlabel(r'$|A \cup B|$', fontsize='23')
    ax.xaxis.set_label_coords(0.5, -0.13)
    if i==0:
        ax.set_ylabel(r'$J(A,B)$', fontsize='23')
    else:
        ax.set_ylabel(r'$S(A,B)$', fontsize='23')

    ax.yaxis.set_label_coords(-0.15, 0.5)
    # plt.legend(prop={'size':8},loc='upper right')
    # plt.legend(bbox_to_anchor=(1.00, 1), loc=2, borderaxespad=0.)
    plt.savefig('{0}_edge_01.png'.format(kind))
    # plt.savefig('{0}_edge.eps'.format(kind))
