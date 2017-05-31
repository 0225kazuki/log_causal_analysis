#!/usr/bin/python

import numpy as np
import pandas as pd
import datetime
import search_burst as sb
import plot_day
import pickle


def ev2dumpname(ev):
    idnum=int(ev.split("_")[0])
    if idnum<500:
        return('rplinear/dumps_rplinear/0000-0499/'+ev+'.dump')
    elif idnum<1000:
        return('rplinear/dumps_rplinear/0500-0999/'+ev+'.dump')
    elif idnum<1500:
        return('rplinear/dumps_rplinear/1000-1499/'+ev+'.dump')
    elif idnum<2000:
        return('rplinear/dumps_rplinear/1500-1999/'+ev+'.dump')

def cnt_logs(DUMP_NAME,DATE):
    with open(DUMP_NAME,"rb") as f: 
        obj = pickle.load(f, encoding="bytes")

    plot_year = int(DATE[:4])
    plot_month = int(DATE[4:6])
    plot_day = int(DATE[6:8])

    plot_date = datetime.date(plot_year,plot_month,plot_day)

    plot_data = [row for row in obj if row.date() == plot_date]
    return(len(plot_data))


if __name__ == "__main__":

    bursts = sb.open_dump('rplinear/burst_rp_df')
    p_burst_pair = sb.open_dump('rplinear/partial_coburst_event.dump')

    result=[]
    for burst_ev,causal_ev in p_burst_pair:
        dates = [i.strftime('%Y%m%d') for i in bursts[burst_ev].dropna().index]
        for date in dates:
            if cnt_logs(ev2dumpname(causal_ev),date) != 0:
                result.append((burst_ev,causal_ev,date))



    print(result)
            # try:
            #     plot_day.plot_day(ev2dumpname(causal_ev),date)
            # except:
            #     print('error',causal_ev,date)
