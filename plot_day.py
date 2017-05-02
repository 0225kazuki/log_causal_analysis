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



if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('usage \n python plot_day.py xxxx.dump 20120101')
        exit()

    DUMP_NAME = sys.argv[1]
    DATE = sys.argv[2]
    plot_day(DUMP_NAME, DATE)
