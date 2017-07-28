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
# import search_burst as sb
import os.path

def open_dump(dump_file):
    with open(dump_file, "rb") as f:
        obj = pickle.load(f, encoding="bytes")
    return obj

def get_dump_path(DUMP_NAME, DATE):
    path = 'dumps/'+DATE+'/'+DUMP_NAME
    if os.path.exists(path):
        return path
    else:
        print('file not exist')
        exit()

def plot_day(DUMP_NAME, DATE):

    if "/" in DUMP_NAME:
        obj = open_dump(DUMP_NAME)
    else:
        obj =   open_dump(get_dump_path(DUMP_NAME,DATE))

    plot_year = int(DATE[:4])
    plot_month = int(DATE[4:6])
    plot_day = int(DATE[6:8])

    plot_date = datetime.date(plot_year,plot_month,plot_day)

    plot_data = [row for row in obj if row.date() == plot_date]
    # print(plot_data)
    # plot_data = [row.time() for row in obj if row.date() == plot_date]
    plot_data = [row.time() for row in obj]
    plot_data_coll = collections.Counter(plot_data)

    x = [row.hour*3600 + row.minute*60 + row.second for row in sorted(set(plot_data))]

    y = [0]
    for row in sorted(plot_data_coll.items(),key=lambda z:z[0]):
        y.append(row[1]+y[-1])
    y = y[1:]

    # 階段状にする処理
    x = np.sort(np.append(x,x))[1:]
    x = np.insert(x,0,x[0])

    tmp = []
    for row in y:
        tmp.append(row)
        tmp.append(row)

    y = tmp[:-1]
    y = [0] + y

    # plot
    fig = plt.figure(figsize=(30,10))
    #default left : 0.125　right : 0.9　bottom : 0.1　top : 0.9　wspace : 0.2　hspace : 0.2
    fig.subplots_adjust(left=0.03,right=0.999)

    plt.title(DUMP_NAME+"\t"+DATE)

    plt.plot(x, y)
    plt.xticks([i*3600 for i in range(25)],[str(i).zfill(2)+':00\n{0}'.format(i*3600) for i in range(25)],fontsize=25,rotation=90)
    plt.yticks(fontsize=25)

    plt.xlim(0,86400)
    # plt.grid()

    # plt.savefig(DUMP_NAME.split('/')[-1].split('.')[0]+'_'+DATE+'.png')
    plt.show()

def plot_day_old(DUMP_NAME, DATE):

    obj = open_dump(DUMP_NAME)

    plot_year = int(DATE[:4])
    plot_month = int(DATE[4:6])
    plot_day = int(DATE[6:8])

    plot_date = datetime.date(plot_year,plot_month,plot_day)

    plot_data = [row for row in obj if row.date() == plot_date]
    print(plot_data)
    # plot_data = [row.time() for row in obj if row.date() == plot_date]
    plot_data = [row.time() for row in obj]
    plot_data_coll = collections.Counter(plot_data)

    x = [row.hour*3600 + row.minute*60 + row.second for row in sorted(set(plot_data))]

    y = [0]
    for row in sorted(plot_data_coll.items(),key=lambda z:z[0]):
        y.append(row[1]+y[-1])
    y = y[1:]

    # 階段状にする処理
    x = np.sort(np.append(x,x))[1:]
    x = np.insert(x,0,x[0])

    tmp = []
    for row in y:
        tmp.append(row)
        tmp.append(row)

    y = tmp[:-1]
    y = [0] + y

    # データをセット
    fig = plt.figure(figsize=(12,8))
    #default left : 0.125　right : 0.9　bottom : 0.1　top : 0.9　wspace : 0.2　hspace : 0.2
    fig.subplots_adjust(top=0.95, bottom=0.15, left=0.15)

    ax = fig.add_subplot(111)
    plt.plot(x, y, lw=3)
    plt.xticks([i*3600 for i in range(25)][::2],[str(i).zfill(2) for i in range(25)][::2],rotation=90,fontsize='20')
    plt.yticks(fontsize='25')

    # print(x)
    # for st in set(x):
    #     plt.plot([st,st], [0,max(y)*1.05], "--", color='red', alpha=0.3)
        # plt.bar(st, max(y)*1.05)
        # plt.plot([en,en], [0,max(y)*1.05], "--", color='orange', alpha=0.3)
        # plt.fill([st,en,en,st], [0,0,max(y)*1.05,max(y)*1.05], color='#D0D0D0', alpha=0.1)
        # plt.fill([st,en,en,st], [0,0,max(y)*1.05,max(y)*1.05], color='#505050', alpha=0.1)

    plt.xlabel('time', fontsize='23')
    ax.xaxis.set_label_coords(0.5, -0.13)
    ax.set_ylabel('Cumulative Count', fontsize='23')

    plt.xlim(0,86400)
    plt.ylim(0,max(y)*1.05)
    plt.grid()
    plt.savefig(DUMP_NAME.split('/')[-1].split('.')[0]+'_'+DATE+'.png')

def plot_day_fp(DUMP_NAME, DATE):

    obj = open_dump(get_dump_path(DUMP_NAME,DATE))

    plot_year = int(DATE[:4])
    plot_month = int(DATE[4:6])
    plot_day = int(DATE[6:8])

    plot_date = datetime.date(plot_year,plot_month,plot_day)
    plot_data = [row for row in obj if row.date() == plot_date]

    plot_data = [row.time() for row in obj if row.date() == plot_date]

    plot_data_coll = collections.Counter(plot_data)

    x = [row.hour*3600 + row.minute*60 + row.second for row in sorted(set(plot_data))]
    y = [0]
    for row in sorted(plot_data_coll.items(),key=lambda z:z[0]):
        y.append(row[1]+y[-1])
    y = y[1:]

    # 階段状にする処理
    x = np.sort(np.append(x, x))[1:]
    x = np.insert(x, 0, x[0])
    x = np.append(x, 86399)

    tmp = []
    for row in y:
        tmp.append(row)
        tmp.append(row)

    y = tmp[:-1]
    y = [0] + y + [y[-1]]


    # データをセット
    fig = plt.figure(figsize=(12,8))
    #default left : 0.125　right : 0.9　bottom : 0.1　top : 0.9　wspace : 0.2　hspace : 0.2
    fig.subplots_adjust(top=0.95, bottom=0.15, left=0.15)

    # for st,en in tmp:
        # plt.plot([st,st], [0,max(y)*1.05], "--", color='red', alpha=0.3)
        # plt.bar(st, max(y)*1.05)
        # plt.plot([en,en], [0,max(y)*1.05], "--", color='orange', alpha=0.3)
        # plt.fill([st,en,en,st], [0,0,max(y)*1.05,max(y)*1.05], color='#D0D0D0', alpha=0.1)
        # plt.fill([st,en,en,st], [0,0,max(y)*1.05,max(y)*1.05], color='#505050', alpha=0.1)

    ax = fig.add_subplot(111)

    plt.title(DUMP_NAME+"\t"+DATE)

    plt.plot(x, y, lw=3)
    plt.xticks([i*3600 for i in range(25)][::2],[str(i).zfill(2) for i in range(25)][::2],rotation=90,fontsize='20')
    # plt.xticks([i*3600 for i in range(25)],[str(i).zfill(2) for i in range(25)],rotation=90,fontsize='20')
    plt.yticks(fontsize='25')

    # plt.title('Ex.5', fontsize='20')

    plt.xlabel('time', fontsize='23')
    ax.xaxis.set_label_coords(0.5, -0.13)
    ax.set_ylabel('Cumulative Count', fontsize='23')
    # ax.yaxis.set_label_coords(-0.15, 0.5)
    # plt.ylabel('Cumulative Count', fontsize='20', x=-50000)

    plt.xlim(0,86400)
    plt.ylim(0,max(y)*1.05)
    plt.grid()
    plt.savefig(DUMP_NAME.split('/')[-1].split('.')[0]+'_'+DATE+'.png')
    # plt.savefig(DUMP_NAME.split('/')[-1].split('.')[0]+'_'+DATE+'.eps')

def plot_day_comp(DUMP_NAME1, DUMP_NAME2, DATE):

    # plot
    fig = plt.figure(figsize=(18,10))
    #default left : 0.125　right : 0.9　bottom : 0.1　top : 0.9　wspace : 0.2　hspace : 0.2
    fig.subplots_adjust(left=0.03,right=0.999, hspace=0.5)
    plot_cnt = 1
    for DUMP_NAME in [DUMP_NAME1,DUMP_NAME2]:
        obj = open_dump(get_dump_path(DUMP_NAME,DATE))

        plot_year = int(DATE[:4])
        plot_month = int(DATE[4:6])
        plot_day = int(DATE[6:8])
        plot_date = datetime.date(plot_year,plot_month,plot_day)

        plot_data = [row.time() for row in obj if row.date() == plot_date]
        plot_data_coll = collections.Counter(plot_data)

        x = [row.hour*3600 + row.minute*60 + row.second for row in sorted(set(plot_data))]

        y = [0]
        for row in sorted(plot_data_coll.items(),key=lambda z:z[0]):
            y.append(row[1]+y[-1])
        y = y[1:]

        x = np.sort(np.append(x,x))[1:]
        x = np.insert(x,0,x[0])

        tmp = []
        for row in y:
            tmp.append(row)
            tmp.append(row)

        y = tmp[:-1]
        y = [0] + y

        plt.subplot(2,1,plot_cnt)

        plt.plot(x, y)
        plt.xticks([i*3600 for i in range(25)],[str(i).zfill(2)+':00\n{0}'.format(i*3600) for i in range(25)],rotation=90)

        plt.title(DUMP_NAME.split('/')[-1], fontsize=('20'))
        plt.xlim(0,86400)
        plt.grid()

        plot_cnt += 1

    plt.savefig(DUMP_NAME1.split('/')[-1].split('.')[0]+'-'+DUMP_NAME2.split('/')[-1].split('.')[0]+'_'+DATE+'.png')


def plot_day_comp_fp(DUMP_NAME1, DUMP_NAME2, DATE, DIRECTION):

    if DIRECTION == '1':
        title = ['Sorce','Destination']
    elif DIRECTION == '0':
        title = ['No Direction Ditected','']
    else:
        title = ['','']

    # plot
    fig = plt.figure(figsize=(14,12))
    #default left : 0.125　right : 0.9　bottom : 0.1　top : 0.9　wspace : 0.2　hspace : 0.2
    fig.subplots_adjust(left=0.08,right=0.99, hspace=0.5, bottom=0.13, top=0.95)
    plot_cnt = 1
    for DUMP_NAME in [DUMP_NAME1,DUMP_NAME2]:
        obj = open_dump(get_dump_path(DUMP_NAME,DATE))

        plot_year = int(DATE[:4])
        plot_month = int(DATE[4:6])
        plot_day = int(DATE[6:8])
        plot_date = datetime.date(plot_year,plot_month,plot_day)

        plot_data = [row.time() for row in obj if row.date() == plot_date]
        plot_data_coll = collections.Counter(plot_data)

        x = [row.hour*3600 + row.minute*60 + row.second for row in sorted(set(plot_data))]

        y = [0]
        for row in sorted(plot_data_coll.items(),key=lambda z:z[0]):
            y.append(row[1]+y[-1])
        y = y[1:]

        x = np.sort(np.append(x,x))[1:]
        x = np.insert(x,0,x[0])

        tmp = []
        for row in y:
            tmp.append(row)
            tmp.append(row)

        y = tmp[:-1]
        y = [0] + y

        x = np.insert(x,0,0)
        x = np.append(x,86399)
        y = [0,] + y + [y[-1]]

        # plt.subplot(2,1,plot_cnt)
        ax = fig.add_subplot(2,1,plot_cnt)
        plt.plot(x, y)
        plt.xticks([i*3600 for i in range(25)],[str(i).zfill(2)+':00' for i in range(25)],rotation=90,fontsize=15)
        plt.xlabel('Time',fontsize=('20'))
        ax.xaxis.set_label_coords(0.5, -0.25)
        plt.yticks(fontsize=15)
        plt.ylabel('Cumulative Count',fontsize=('20'))

        plt.title(title[plot_cnt-1], fontsize=('20'))
        plt.xlim(0,86400)
        plt.grid()

        plot_cnt += 1

    plt.savefig(DUMP_NAME1.split('/')[-1].split('.')[0]+'-'+DUMP_NAME2.split('/')[-1].split('.')[0]+'_'+DATE+'.png')

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('usage')
        print('Plot:\t\tpython plot_day.py event 20120101')
        print('For Paper plot:\tpython plot_day.py event 20120101 p')
        print('Double plot:\tpython plot_day.py event1 event2 20120101')
        exit()

    if len(sys.argv) == 4 and sys.argv[-1] == 'p':
        # for paper fig plot
        DUMP_NAME = sys.argv[1]
        DATE = sys.argv[2]
        plot_day_fp(DUMP_NAME, DATE)
    elif len(sys.argv) == 4 and sys.argv[-1] == 'old':
        DUMP_NAME = sys.argv[1]
        DATE = sys.argv[2]
        plot_day_old(DUMP_NAME, DATE)
    elif len(sys.argv) == 4:
        DUMP_NAME1 = sys.argv[1]
        DUMP_NAME2 = sys.argv[2]
        DATE = sys.argv[3]
        plot_day_comp(DUMP_NAME1, DUMP_NAME2, DATE)
    elif len(sys.argv) == 5:
        DUMP_NAME1 = sys.argv[1]
        DUMP_NAME2 = sys.argv[2]
        DATE = sys.argv[3]
        plot_day_comp_fp(DUMP_NAME1, DUMP_NAME2, DATE, sys.argv[4])
    else:
        DUMP_NAME = sys.argv[1]
        DATE = sys.argv[2]
        plot_day(DUMP_NAME, DATE)
