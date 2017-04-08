#!/usr/bin/python
# coding: UTF-8

'''
dumpから日毎の累積度数をプロット

python plot.py xxxx.dump
'''

import collections
import pprint
import re
import sys
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import pybursts
import math
import time
import datetime
import matplotlib.dates as mdates
import pickle


DUMP_NAME = sys.argv[1]

with open(DUMP_NAME,"rb") as f:
    obj = pickle.load(f, encoding="bytes")


tmp = set( [datetime.datetime(row.year,row.month,row.day) for row in obj ] )
x = sorted(list(tmp))
print(x)

# Y軸データ
y = sorted(collections.Counter([row.date() for row in obj]).items(),key=lambda x:x[0])
y = [row[1] for row in y]

print(y)

# if max(y) < 1000:
#     exit()

# データをセット
# fig = plt.figure(figsize=(30,10))
# #default left : 0.125　right : 0.9　bottom : 0.1　top : 0.9　wspace : 0.2　hspace : 0.2
# fig.subplots_adjust(left=0.03,right=0.999)

# データをセット
fig = plt.figure(figsize=(30,10))
# ax = fig.add_subplot(111)
fig.subplots_adjust(left=0.03,right=0.995)

plt.bar(x, y, color='b',edgecolor='b')

xticks_label = [datetime.date(2012,i,1)for i in range(1,13)] + [datetime.date(2013,i,1) for i in range(1,5)]
plt.xticks(xticks_label,xticks_label)

print(xticks_label[-1])
plt.xlim(xticks_label[0],xticks_label[-1])
plt.grid(b=True, which='major',color='black',lw='1')
# plt.grid(b=True, which='minor',color='gray')

# グラフのフォーマットの設定
# days = mdates.DayLocator()  # every second
# daysFmt = mdates.DateFormatter('%Y-%m-%d')
# ax.xaxis.set_major_locator(days)
# ax.xaxis.set_major_formatter(daysFmt)
# fig.autofmt_xdate()

print(DUMP_NAME.split('/')[-1].split('.')[0]+'.png')
plt.savefig(DUMP_NAME.split('/')[-1].split('.')[0]+'.png')



exit()
