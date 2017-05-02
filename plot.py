#!/usr/bin/python
# coding: UTF-8

'''
dumpから日毎の累積度数をプロット


python plot.py xxxx.dump
'''

import collections
import sys
import numpy as np
import matplotlib.pyplot as plt
import pybursts
import datetime
import matplotlib.dates as mdates
import pickle
import plot_day

def burst2get_data(burst_file):
    # print(burst_file)
    get_data = collections.defaultdict(lambda: 0)
    for line in open(burst_file,"r"):
        if line[0] == '(':
            get_date = "".join([a.strip().zfill(2) for a in line[1:-2].split(",")])
            get_data[get_date] = []
        elif line.strip()[0] == "[":
            st = line.strip()[1:-2].split(",")[1].strip()
            en = line.strip()[1:-2].split(",")[2].strip()
            get_data[get_date].append((float(st),float(en)))

    return get_data


DUMP_NAME = sys.argv[1]
if len(sys.argv) > 2:
    PLOT_BURST = int(sys.argv[2])
else:
    PLOT_BURST = 0

with open(DUMP_NAME,"rb") as f:
    obj = pickle.load(f, encoding="bytes")


tmp = set( [datetime.datetime(row.year,row.month,row.day) for row in obj ] )
x = sorted(list(tmp))
# print(x)

# Y軸データ
y = sorted(collections.Counter([row.date() for row in obj]).items(),key=lambda x:x[0])
y = [row[1] for row in y]

# print(y)

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

# print(xticks_label[-1])
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

if PLOT_BURST == 1:
    burst_days=burst2get_data('burst_rplinear_0000-0499/'+DUMP_NAME.split('/')[-1]+'.txt').keys()
    print(burst_days)
    # exit()
    for burst_day in burst_days:
        plot_day.plot_day(DUMP_NAME,burst_day)


exit()
