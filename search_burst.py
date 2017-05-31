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
import matplotlib
import matplotlib.pyplot as plt
# import seaborn as sns

def print_full(x):
    pd.set_option('display.max_rows', len(x))
    pd.set_option('display.max_columns', len(x.columns))
    print(x)
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')


def open_dump(dump_file):
    with open(dump_file, "rb") as f:
        obj = pickle.load(f, encoding="bytes")
    return obj


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
                            break # cur_event1つにつき関連eventは重複して数えない
            if co_burst_results[cur_event] == 0:
                co_burst_results[cur_event] = collections.Counter(rel_event)
            else:
                print('ck')
                co_burst_results[cur_event] += collections.Counter(rel_event)

    return co_burst_results



def calc_jaccard(AandB, A, B):
    AorB = A + B - AandB
    if AorB == 0:
        return 1.0
    else:
        prb = AandB / AorB
        if prb > 1. :
            prb = 1.
        return prb


def calc_simpson(AandB, A, B):
    prb = AandB / min(A,B)
    if prb > 1. :
        prb = 1.
    return prb


def calc_co_prob(host_bursts, cur_event, co_result):
    cur_all = host_bursts[cur_event]

    co_prob_result = pd.DataFrame(columns=['x','y_jaccard','y_simpson'])

    for co_event, co_cnt in co_result:
        new_line = pd.Series(name=co_event, index=['x','y_jaccard','y_simpson'])

        new_line['x'] = host_bursts[co_event]

        co_event_all = host_bursts[co_event]
        new_line['y_jaccard'] = calc_jaccard(co_cnt, cur_all, co_event_all)
        new_line['y_simpson'] = calc_simpson(co_cnt, cur_all, co_event_all)

        co_prob_result = co_prob_result.append(new_line)

    return co_prob_result


def calc_co_prob_all(host_bursts, co_burst_results):
    event_set = []

    co_prob_result = pd.DataFrame(columns=['EvPair', 'x', 'y_jaccard', 'y_simpson'])

    for cur_event, co_result in co_burst_results.items():
        cur_all = host_bursts[cur_event]
        for co_event, co_cnt in co_result.items():
            if {cur_event, co_event} in event_set:
                continue
            if co_burst_results[co_event][cur_event] > co_cnt: #もし関連event側からみて&が多かったら入れ替え
                co_cnt = co_burst_results[co_event][cur_event]
            # else:
            event_set.append({cur_event, co_event})
            co_all = host_bursts[co_event]

            new_line = pd.Series(index=['EvPair', 'x', 'y_jaccard', 'y_simpson'])

            new_line['EvPair'] = (cur_event, co_event)
            new_line['x'] = co_all + cur_all - co_cnt
            new_line['y_jaccard'] = calc_jaccard(co_cnt, cur_all, co_all)
            new_line['y_simpson'] = calc_simpson(co_cnt, cur_all, co_all)

            if new_line['y_jaccard'] > 1 or new_line['y_simpson'] > 1:
                print(new_line, co_all, cur_all, co_cnt)

            co_prob_result = co_prob_result.append(new_line, ignore_index=True)

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

    if len(co_prob_result) == 0 :
        return 0

    fig = plt.figure()

    plt.style.use('ggplot')
    # fig.subplots_adjust(left=0.03,right=0.995)

    co_prob_result['y_jaccard'] = co_prob_result['y_jaccard'] * (10 ** 5 )
    co_prob_result.plot(kind='scatter',x='x', y='y_jaccard', figsize=(9,9))

    plt.title(cur_event, fontsize='20')

    plt.xscale("log")
    plt.yscale("log")

    plt.xticks(fontsize='15')
    # plt.xlabel(fontsize='15')
    plt.yticks([10 ** i for i in range(1,6)],
               ['$1.0^{-4}$','$1.0^{-3}$','$1.0^{-2}$','$1.0^{-1}$','1.0'],
               fontsize='15')
    # plt.ylabel(fontsize='15')

    plt.ylim(1., 10. ** 5 + 10 ** 4)
    plt.grid(b=True, which='major',lw='1', color='gray')
    plt.grid(b=True, which='minor', linestyle='--', color='white')

    plt.savefig('{0}_jaccard.png'.format(cur_event))


def co_plot_all(co_prob_result):

    if len(co_prob_result) == 0 :
        return 0

    fig = plt.figure()

    plt.style.use('ggplot')
    # fig.subplots_adjust(left=0.03,right=0.995)

    plot_cnt = 1
    # co_prob_result.plot(subplots=True,layout=(1,3))
    fig, axes = plt.subplots(nrows=1,ncols=2)
    for kind in ['jaccard','simpson']:
        # plt.subplot(1,2,plot_cnt)
        co_prob_result['y_{0}'.format(kind)] = co_prob_result['y_{0}'.format(kind)] * (10 ** 5 )
        # co_prob_result['y_simpson'] = co_prob_result['y_simpson'] * (10 ** 5 )

        co_prob_result.plot(kind='scatter',x='x', y='y_{0}'.format(kind), figsize=(9,9))
        # co_prob_result.plot(kind='scatter', figsize=(9,9), subplots= True, layout=(1,2), x='x', y ='y_jaccard')

        # plt.xscale("log")
        plt.yscale("log")

        plt.xticks(fontsize='15')
        plt.yticks([10 ** i for i in range(1,6)],
                   ['$1.0^{-4}$','$1.0^{-3}$','$1.0^{-2}$','$1.0^{-1}$','1.0'],
                   fontsize='15')
        # plt.yticks(fontsize='15')

        plt.ylim(1., 10. ** 5 + 10 ** 4)
        # plt.ylim(-1000, 10. ** 5 + 10 ** 4)
        plt.grid(b=True, which='major',lw='1', color='gray')
        plt.grid(b=True, which='minor', linestyle='--', color='white')
        plot_cnt += 1

        plt.savefig('{0}_all.png'.format(kind))


def co_plot_all_fp(co_prob_result):
    if len(co_prob_result) == 0 :
        return 0

    plot_cnt = 1
    for kind in ['jaccard','simpson']:

        fig = plt.figure(figsize=(10,6))
        ax = fig.add_subplot(111)
        fig.subplots_adjust(top=0.95, bottom=0.15, left=0.15)

        co_prob_result['y_{0}'.format(kind)] = co_prob_result['y_{0}'.format(kind)] * (10 ** 5 )

        x=co_prob_result['x'].values
        y=co_prob_result['y_{0}'.format(kind)].values

        plt.scatter(x,y, marker='.', c=None)

        plt.yscale("log")

        plt.xticks(fontsize='18')
        plt.yticks([10 ** i for i in range(1,6)],
                   ['$1.0^{-4}$','$1.0^{-3}$','$1.0^{-2}$','$1.0^{-1}$','1.0'],
                   fontsize='25')

        plt.ylim(1., 10. ** 5 + 10 ** 4)
        plt.grid()

        plt.xlabel(r'$|A \cup B|$', fontsize='23')
        ax.xaxis.set_label_coords(0.5, -0.13)
        if plot_cnt==1:
            ax.set_ylabel(r'$J(A,B)$', fontsize='23')
        else:
            ax.set_ylabel(r'$S(A,B)$', fontsize='23')

        ax.yaxis.set_label_coords(-0.15, 0.5)
        plt.savefig('{0}_nofilter.eps'.format(kind))

        plot_cnt += 1


if __name__ == "__main__":
    if len(sys.argv) == 2:
        burst_df = open_dump(sys.argv[1])
        ind = burst_df.index

        host_bursts = host_burst_cnt(burst_df)

        co_burst_results = search_burst(burst_df)

        co_prob_result = calc_co_prob_all(host_bursts, co_burst_results)
        co_prob_result = co_prob_result.sort_values(by='y_jaccard', ascending=False)

        with open('co_prob_df','wb') as f:
            pickle.dump(co_prob_result,f)

        co_plot_all(co_prob_result)
        # print_full(co_prob_result.sort_values(by='b', ascending=False))

        exit()
        for cur_event, co_result in co_burst_results.items():
            co_result = sorted(co_result.items(),
                               key=lambda x: x[1],
                               reverse=True)

            co_prob_result = calc_co_prob(host_bursts, cur_event, co_result)

            print('\nind:',cur_event,host_bursts[cur_event])
            print_full(co_prob_result)
            co_plot(cur_event,co_prob_result)

    else:
        co_prob_result = open_dump(sys.argv[2])
        print_full(co_prob_result)
        co_plot_all(co_prob_result)
