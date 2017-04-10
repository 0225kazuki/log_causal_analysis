import pickle
import datetime
import sys
import glob
import collections
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


'''

'''


def create_xy(dump_name,get_date):
    #特定日の累積和プロット用の階段処理してあるx, yを生成
    obj = open_dump(dump_name)

    plot_year = int(get_date[:4])
    plot_month = int(get_date[4:6])
    plot_day = int(get_date[6:8])

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

    if x[-1] != 86399:
        x = np.append(x,86399)
        y = np.append(y,y[-1])

    return (x,y)

def print_full(x):
    pd.set_option('display.max_rows', len(x))
    pd.set_option('display.max_columns', len(x.columns))
    print(x)
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')

def open_dump(dump_file):
    with open(dump_file,"rb") as f:
        obj = pickle.load(f, encoding="bytes")
    return obj

def get_most_ids(df,get_date):
    #dfから特定日の大量発生しているIDを降順に取得 -> ids
    id_sr = df.loc[get_date]
    # id_sr.sort(ascending=False)
    id_sr = id_sr.sort_values(inplace=False, ascending=False)
    id_sr = id_sr.dropna()

    ids = id_sr.index

    print(id_sr)
    return ids

def burst2get_dates(burst_file):
    get_dates = []
    for line in open(burst_file,"r"):
        if line[0] == '(':
            get_date = "".join([a.strip().zfill(2) for a in line[1:-2].split(",")])
            get_dates.append(get_date)
        else:
            continue

    return get_dates

#日毎に前後60secで発生しているバースト結果を検索
def search_burst(day_series):
    for i,j in day_series.iteritems():
        print('\n',i)
        for cur in j:
            cur_st = cur[0]
            for k,l in day_series.iteritems():
                if k == i:
                    continue
                for tar in l:
                    tar_st = tar[0]
                    if cur_st - 60 < tar_st < cur_st + 60:
                        print('hit','\n',i,cur_st,'\n',k,tar_st)
    return 0

def search_burst2(day_series):
    returns = collections.defaultdict(lambda: 0)
    for cur_event,cur_values in day_series.iteritems():
        rel_event = []
        for cur in cur_values:
            cur_st = cur[0]
            for tar_event,tar_values in day_series.iteritems():
                if tar_event == cur_event:
                    continue
                for tar in tar_values:
                    tar_st = tar[0]
                    if cur_st - 60 < tar_st < cur_st + 60:
                        rel_event.append(tar_event)
        # print(cur_event,'\n',collections.Counter(rel_event))
        returns[cur_event] = collections.Counter(rel_event)
    return returns

if __name__ == "__main__":
    burst_df = open_dump("./nofilter/burst_df.dump")
    ind = burst_df.index
    result = collections.defaultdict(lambda: 0)
    for ii in ind:
        tmp = burst_df.loc[ii]
        tmp2 = tmp.dropna()
        # print(ii)
        returns = search_burst2(tmp2)
        for i,j in returns.items():
            if result[i] == 0:
                result[i] = j
            else:
                result[i] += j

    for i,j in result.items():
        print('\n',i,sorted(j.items(),key=lambda x:x[1],reverse=True))
