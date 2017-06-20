#!/usr/bin/python

import numpy as np
import pandas as pd
import datetime
import search_burst as sb
import plot_day
import pickle
import search_burst as sb
import sqlite3
import glob

'''
log情報を得るやつ
'''


def cnt_logs(DUMP_NAME,DATE):
    obj = sb.open_dump(DUMP_NAME)
    return(len(obj))


def get_eday(evp):
    argv = []
    argv.extend(evp[0].split("_"))
    argv.extend(evp[1].split("_"))
    # print(argv)
    query='select date from date where pairID in(select pairID from event where (srcID={0} and srcHost="{1}" and dstID={2} and dstHost="{3}") or (srcID={2} and srcHost="{3}" and dstID={0} and dstHost="{1}"));'.format(argv[0],argv[1],argv[2],argv[3])
    cur.execute(query)
    r  = cur.fetchall()
    # print(r)
    result = []
    for i in r:
        result.append("".join(i[0].split("-")))
    return result

if __name__ == "__main__":
    dates = [x.split('/')[-1] for x in glob.glob('dumps/*')]

    av_cnt = np.array([])
    for date in dates:
        files = glob.glob('dumps/{0}/*'.format(date))
        date_log_cnt = 0
        for fi in files:
            date_log_cnt += cnt_logs(fi,date)
        av_cnt = np.append(av_cnt, date_log_cnt)

    print(np.average(av_cnt))
