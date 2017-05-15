# -*- coding: utf-8 -*-
from scipy import arange, hamming, sin, pi
from scipy.fftpack import fft, ifft, fftfreq
import matplotlib.pyplot as plt
import search_burst as sb
import numpy as np
import pandas as pd
import sys
import datetime
import collections
import glob

# 誤差が高いほど周期関係ない
def linear_rms(event, ev_day):
    day = ev_day
    ev_year = int(day[:4])
    ev_month = int(day[4:6])
    ev_day = int(day[6:8])

    ev_date = datetime.date(ev_year,ev_month,ev_day)
    ev_data = [row.time() for row in event if row.date() == ev_date]

    ev_data_coll = collections.Counter(ev_data)

    x = [row.hour*3600 + row.minute*60 + row.second for row in sorted(set(ev_data))]

    if len(x) < 10:
        return 1

    y = [0]
    for row in sorted(ev_data_coll.items(),key=lambda z:z[0]):
        y.append(row[1]+y[-1])
    y = y[1:]

    a=len(ev_data)/86400
    linx=x

    liny=[a * i for i in linx]

    # print(ev_data[:40])
    #
    # for e in range(len(y)):
    #     print(x[e],y[e],liny[e])

    return sum([ abs(a-b) for a,b in zip(liny,y) ]) / len(liny) / len(ev_data)

def get_dump_path(ev_name):
    pf = './'
    temp_id = int(ev_name.split('_')[0])
    if temp_id < 500:
        return pf + '0000-0499/' + ev_name + '.dump'
    elif temp_id < 1000:
        return pf + '0500-0999/' + ev_name + '.dump'
    elif temp_id <  1500:
        return pf + '1000-1499/' + ev_name + '.dump'
    else:
        return pf + '1500-1999/' + ev_name + '.dump'

if __name__ == "__main__":
    if len(sys.argv) == 3:
        dump = sys.argv[1]
        ev_day = sys.argv[2]
        event = sb.open_dump(dump)
        print(linear_rms(event, ev_day))

    else:
        burst_df = sb.open_dump(sys.argv[1])
        for i in burst_df.iteritems():
            tmp = i[1].dropna()
            if len(tmp) != 0 :
                print(tmp.name)
                dump_name = get_dump_path(tmp.name)
                event = sb.open_dump(dump_name)
                for ev_day in tmp.index:
                    rms = linear_rms(event, ev_day.strftime('%Y%m%d'))
                    if not rms > 0.1:
                        print(ev_day,'\t',rms)
