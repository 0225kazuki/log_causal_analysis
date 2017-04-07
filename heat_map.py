#!/usr/bin/python
# coding: UTF-8

'''
引数で与えられたdumpファイルの全体のヒートマップを描画

python heat_map.py xx.dump yy.dump ...
'''

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
import sys
import datetime
import collections




def print_full(x):
    pd.set_option('display.max_rows', len(x))
    pd.set_option('display.max_columns',len(x.columns))
    print(x)
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')


if __name__ == "__main__":
    values = []
    dn_list = []

    for dn in sys.argv[1:]:
        DUMP_NAME = dn
        dn_list.append(dn.split('/')[-1])

        with open(DUMP_NAME,"rb") as f:
            obj = pickle.load(f, encoding="bytes")

        tmp = set( [datetime.datetime(row.year,row.month,row.day) for row in obj ] )
        x = sorted(list(tmp))

        # Y軸データ
        y = sorted(collections.Counter([row.date() for row in obj]).items(),key=lambda x:x[0])
        y = [row[1] for row in y]



        x = [str(z.strftime('%Y-%m-%d')) for z in x]
        z = {str(k)[:10]:0 for k in pd.date_range("20120101",periods=456)}
        for i,j in zip(x,y):
            z[i]=j

        values.append([i[1] for i in sorted(z.items(),key=lambda x:x[0])][:456])




    df = pd.DataFrame(values,columns=pd.date_range("20120101",periods=456),index=dn_list)

    print_full(df)

    # x:date y:eventID のヒートマップ
    #default left : 0.125　right : 0.9　bottom : 0.1　top : 0.9　wspace : 0.2　hspace : 0.2
    fig = plt.figure(figsize=(25,18))
    fig.subplots_adjust(right=0.999)
    # ax = fig.add_subplot(111)

    sns.heatmap(df,cmap="Reds")
    print(x)
    plt.xticks([0,31,59,90,120,151,181,212,243,273,304,334,365,396,426,457],[datetime.date(2012,i,1) for i in range(1,13)]+[datetime.date(2013,i,1) for i in range(1,4)],fontsize='20')
    plt.yticks(fontsize='15',rotation='0')
    plt.grid()

    plt.savefig(dn_list[0].split('_')[0]+'.png')
