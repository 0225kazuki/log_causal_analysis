# coding=utf-8

'''
search burst.py
'''

import collections
import datetime
import pickle
import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
# import seaborn as sns


def print_full(x):
    pd.set_option('display.max_rows', len(x))
    pd.set_option('display.max_columns', len(x.columns))
    print(x)
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')


def open_dump(dump_file):
    # type: (string) -> object
    with open(dump_file, "rb") as f:
        obj = pickle.load(f, encoding="bytes")
    return obj

def burst2get_dates(burst_file):
    get_dates = []
    for line in open(burst_file, "r"):
        if line[0] == '(':
            get_date = "".join([a.strip().zfill(2)
                                for a in line[1:-2].split(",")])
            get_dates.append(get_date)
        else:
            continue

    return get_dates


def search_burst(burst_df):

    '''
    search_burst(pd.DataFrame burst_df)

    return co_burst_results = dict{
                                   key   = key_event,
                                   value = dict{key   = co_event,
                                                value = cnt}
                                   }
    '''

    co_burst_results = collections.defaultdict(lambda: 0)
    for day_series in burst_df.iterrows():
        # print(type(day_series[1]))
        day_series = day_series[1].dropna()

        for cur_event, cur_values in day_series.iteritems():
            rel_event = []
            for cur in cur_values:
                cur_st = cur[0]
                for tar_event, tar_values in day_series.iteritems():
                    if tar_event == cur_event:
                        continue
                    for tar in tar_values:
                        tar_st = tar[0]
                        if cur_st - 60 < tar_st < cur_st + 60:
                            rel_event.append(tar_event)

            if co_burst_results[cur_event] == 0:
                co_burst_results[cur_event] = collections.Counter(rel_event)
            else:
                co_burst_results[cur_event] += collections.Counter(rel_event)

    return co_burst_results



def calc_jaccard(AandB, A, B):
    AorB = A + B - AandB
    if AorB == 0:
        return 1.0
    else:
        return AandB / AorB


def calc_simpson(AandB, A, B):
    return AandB / min(A,B)


def calc_co_prob(host_bursts, cur_event, co_result):
    cur_all = host_bursts[cur_event]

    # co_prob_result = collections.defaultdict(lambda x: 0)
    co_prob_result = pd.DataFrame(columns=['x','y_jaccard','y_simpson'])

    for co_event, co_cnt in co_result:
        new_line = pd.Series(name=co_event, index=['x','y_jaccard','y_simpson'])

        new_line['x'] = host_bursts[co_event]

        co_event_all = host_bursts[co_event]
        new_line['y_jaccard'] = calc_jaccard(co_cnt, cur_all, co_event_all)
        new_line['y_simpson'] = calc_simpson(co_cnt, cur_all, co_event_all)

        co_prob_result = co_prob_result.append(new_line)
        print(co_prob_result)

    return co_prob_result


def host_burst_cnt(burst_df):

    '''
    host_burst_cnt(pd.DataFrame burst_df)

    returns = dict{key=event, value=all_cnt}
    '''

    returns = collections.defaultdict(lambda: 0)
    columns = burst_df.columns

    for event in columns:
        all_cnt = sum([len(i) for i in burst_df.loc[:, event].dropna()])
        returns[event] = all_cnt

    return returns


def co_plot(cur_event, co_prob_result):

    x = np.array(co_prob_result["x"])
    y_jaccard = np.array(co_prob_result["y_jaccard"] * (10 ** 5))
    y_simpson = co_prob_result["y_simpson"]

    # x = [1,2,4,5,6]
    # y_jaccard = [10,20,40,60,90]


    fig = plt.figure(figsize=(12,12))
    ax = fig.add_subplot(111)
    # fig.subplots_adjust(left=0.03,right=0.995)

    print(x[:10],y_jaccard[:10])
    plt.scatter(list(x), list(y_jaccard))
    plt.title(cur_event, fontsize='20')
    # sns.regplot(list(x), list(y_jaccard), ax, fit_reg=False)

    plt.xscale("log")
    plt.yscale("log")

    # xticks_label = [datetime.date(2012,i,1)for i in range(1,13)] + [datetime.date(2013,i,1) for i in range(1,5)]
    # plt.xticks(xticks_label,xticks_label)
    plt.yticks([10 ** i for i in range(1,6)], ['0.0001','0.001','0.01','0.1','1.0'],fontsize='20')

    # plt.xlim(xticks_label[0],xticks_label[-1])
    # plt.ylim(1. ** (-6), 1.)
    plt.grid()
    # plt.grid(b=True, which='major',color='black',lw='1')
    # plt.grid(b=True, which='minor',color='gray')

    # plt.savefig(DUMP_NAME.split('/')[-1].split('.')[0]+'.png')
    plt.savefig('{0}_jaccard.png'.format(cur_event))


if __name__ == "__main__":
    if len(sys.argv) == 2:
        burst_df = open_dump(sys.argv[1])
        ind = burst_df.index

        host_bursts = host_burst_cnt(burst_df)

        co_burst_results = search_burst(burst_df)

        for cur_event, co_result in co_burst_results.items():
            co_result = sorted(co_result.items(),
                               key=lambda x: x[1],
                               reverse=True)

            co_prob_result = calc_co_prob(host_bursts, cur_event, co_result)

            # with open('search_burst_test_xy','wb') as f:
            #     pickle.dump(co_prob_result,f)

            co_plot(cur_event,co_prob_result)
            # exit()
    else:
        co_prob_result = open_dump(sys.argv[2])
        co_plot('cur_event',co_prob_result)
