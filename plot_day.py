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

def plot_day(DUMP_NAME, DATE):

    with open(DUMP_NAME,"rb") as f:
        obj = pickle.load(f, encoding="bytes")

    plot_year = int(DATE[:4])
    plot_month = int(DATE[4:6])
    plot_day = int(DATE[6:8])

    plot_date = datetime.date(plot_year,plot_month,plot_day)

    # plot_data = [row for row in obj if row.year == plot_year and row.month == plot_month and row.day == plot_day]
    plot_data = [row for row in obj if row.date() == plot_date]

    plot_data = [row.time() for row in obj if row.date() == plot_date]
    # print(plot_data)
    print(len(plot_data))
    print(plot_data[0:50])

    plot_data_coll = collections.Counter(plot_data)

    x = [row.hour*3600 + row.minute*60 + row.second for row in sorted(set(plot_data))]
    # tmp = set( [datetime.datetime(row.year,row.month,row.day) for row in obj ] )
    # x = sorted(list(tmp))


    # Y軸データ
    # y = sorted(collections.Counter([row for row in x]).items(),key=lambda z:z[0])
    # y = [row[1] for row in y]

    # y = [i for i in range(len(x))]

    y = [0]
    for row in sorted(plot_data_coll.items(),key=lambda z:z[0]):
        y.append(row[1]+y[-1])
    y = y[1:]

    # fig = plt.figure(figsize=(25,18))



    # 移動平均
    y_cnt = [(a,b) for a,b in zip(x,y)]

    time_window = 10 * 60 #sec

    sma = []
    for i in range(int(86400/time_window)):
        # sma.append(sum([z[1] for z in y_cnt if time_window * i < z[0] < time_window * (i + 1)])/time_window*60)
        sma_tmp = [z[1] for z in y_cnt if time_window * i < z[0] < time_window * (i + 1)]
        if len(sma_tmp) != 0:
            sma.append(sum(sma_tmp)/len(sma_tmp))
        else:
            sma.append(0)

    sma_x = [i*time_window for i in range(int(86400/time_window))]


    '''
    階段状にする処理
    x = [0,1,2,3,...] -> x = [0,1,1,2,2,3,3,...]
    y = [a,b,c,d,...] -> y = [a,a,b,b,c,c,d,d,...]
    '''
    x = np.sort(np.append(x,x))[1:]
    x = np.insert(x,0,x[0])

    tmp = []
    for row in y:
        tmp.append(row)
        tmp.append(row)

    y = tmp[:-1]
    y = [0] + y


    # データをセット
    fig = plt.figure(figsize=(30,10))
    #default left : 0.125　right : 0.9　bottom : 0.1　top : 0.9　wspace : 0.2　hspace : 0.2
    fig.subplots_adjust(left=0.03,right=0.999)

    # ax = fig.add_subplot(111)
    plt.plot(x, y)
    # plt.bar(x, y, color='blue',edgecolor='blue')
    plt.xticks([i*3600 for i in range(25)],[str(i).zfill(2)+':00\n{0}'.format(i*3600) for i in range(25)],rotation=90)

    # plt.plot(sma_x,sma,color='green')


    plt.xlim(0,86400)
    plt.grid()

    # グラフのフォーマットの設定
    # days = mdates.DayLocator()  # every second
    # daysFmt = mdates.DateFormatter('%Y-%m-%d')
    # ax.xaxis.set_major_locator(days)
    # ax.xaxis.set_major_formatter(daysFmt)
    # fig.autofmt_xdate()


    plt.savefig(DUMP_NAME.split('/')[-1].split('.')[0]+'_'+DATE+'.png')

def plot_day_fp(DUMP_NAME, DATE):

    with open(DUMP_NAME,"rb") as f:
        obj = pickle.load(f, encoding="bytes")

    plot_year = int(DATE[:4])
    plot_month = int(DATE[4:6])
    plot_day = int(DATE[6:8])

    plot_date = datetime.date(plot_year,plot_month,plot_day)
    plot_data = [row for row in obj if row.date() == plot_date]

    plot_data = [row.time() for row in obj if row.date() == plot_date]
    # print(plot_data[0:50])
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
    fig = plt.figure(figsize=(10,6))
    #default left : 0.125　right : 0.9　bottom : 0.1　top : 0.9　wspace : 0.2　hspace : 0.2
    fig.subplots_adjust(top=0.95, bottom=0.15, left=0.15)

    # plt.annotate('burst',xy=(86400/2,30),size=20)

    # 10_hakata-dc-rm 20121120
    # tmp=[[447, 447.33],
    #      [4047, 4048.02],
    #      [7644, 7645.2],
    #      [ 11292, 11293.32],
    #      [14846, 14846.33],
    #      [ 18456, 18456.33],
    #      [ 22045, 22046.12 ],
    #      [ 25644, 25644.33 ],
    #      [ 29248, 29249.06 ],
    #      [ 32847, 32847.33 ],
    #      [ 36441, 36442.31 ],
    #      [ 40049, 40049.33 ],
    #      [ 43650, 43650.33 ],
    #      [ 47247, 47249.07],
    #      [ 50845, 50845.33 ],
    #      [ 54450, 54450.33 ],
    #      [ 58046, 58046.33 ],
    #      [ 61645, 61646.07 ],
    #      [ 65247, 65248.03 ],
    #      [ 68845, 68845.33 ],
    #      [ 72445, 72446.17 ],
    #      [ 76045, 76045.33 ],
    #      [ 79650, 79650.33 ],
    #      [ 81436, 81489],
    #      [ 83243, 83244.16]]

    # 15_sin 20130222
    # tmp = [[306, 43786.01],]

    # 10_wdc 20130316
    # tmp=[[10522, 10624],
    #      [11080, 11148],
    #      [12809, 12853],
    #      [14302, 14343.01]]

    # 30_tokyo-dc-rm 20120111
    tmp=[[37838, 39056.03],
         [39587, 40396.03],
         [40861, 62153.03]]

    # 7_kote 20120116
    # tmp=[[43502, 47107]]
    for st,en in tmp:
        # plt.plot([st,st], [0,max(y)*1.05], "--", color='red', alpha=0.3)
        # plt.bar(st, max(y)*1.05)
        # plt.plot([en,en], [0,max(y)*1.05], "--", color='orange', alpha=0.3)
        plt.fill([st,en,en,st], [0,0,max(y)*1.05,max(y)*1.05], color='#D0D0D0', alpha=0.1)
        # plt.fill([st,en,en,st], [0,0,max(y)*1.05,max(y)*1.05], color='#505050', alpha=0.1)

    ax = fig.add_subplot(111)
    plt.plot(x, y, lw=3)
    plt.xticks([i*3600 for i in range(25)],[str(i).zfill(2) for i in range(25)],rotation=90,fontsize='20')
    plt.yticks(fontsize='25')

    plt.title('Ex.5', fontsize='20')

    plt.xlabel('time', fontsize='23')
    ax.xaxis.set_label_coords(0.5, -0.13)
    ax.set_ylabel('Cumulative Count', fontsize='23')
    ax.yaxis.set_label_coords(-0.15, 0.5)
    # plt.ylabel('Cumulative Count', fontsize='20', x=-50000)

    plt.xlim(0,86400)
    plt.ylim(0,max(y)*1.05)
    plt.grid()
    plt.savefig(DUMP_NAME.split('/')[-1].split('.')[0]+'_'+DATE+'.eps')



if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('usage \n python plot_day.py xxxx.dump 20120101')
        exit()

    if len(sys.argv) == 4 and sys.argv[-1] == 'p':
        # for paper fig plot
        DUMP_NAME = sys.argv[1]
        DATE = sys.argv[2]
        plot_day_fp(DUMP_NAME, DATE)
    else:
        DUMP_NAME = sys.argv[1]
        DATE = sys.argv[2]
        plot_day(DUMP_NAME, DATE)
