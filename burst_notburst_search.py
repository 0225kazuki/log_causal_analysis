#!/usr/bin/python

import numpy as np
import pandas as pd
import datetime
import search_burst as sb
import plot_day
import pickle
import search_burst as sb
import sqlite3

'''
burst - noburstを探す
'''


def cnt_logs(DUMP_NAME,DATE):
    obj = sb.open_dump('dumps/'+str(DATE)+'/'+DUMP_NAME)
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

    dbname = 's4causality.db'
    conn  = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute('''select srcID,srcHost,dstID,dstHost from event''')
    edge = cur.fetchall()
    edge = [sorted((str(e[0])+"_"+e[1],str(e[2])+"_"+e[3])) for e in edge]
    edge = [e[0]+"."+e[1] for e in edge]
    edge = list(set(edge))
    edge = [set(e.split(".")) for e in edge]

    print(len(edge))

    co_burst = sb.open_dump('co_prob_df')
    co_burst = list(co_burst['EvPair'].values)
    co_burst = [set(x) for x in co_burst]

    burst = sb.open_dump('burst_df')
    burst_ev = [x for x in burst.columns if len(burst[x].dropna()) != 0]

    burst_noburst = []
    for ep in edge:
        if ep not in co_burst:
            ep = list(ep)
            if ep[0] in burst_ev:
                burst_noburst.append(ep)
            if ep[1] in burst_ev:
                burst_noburst.append(ep[::-1])


    result = []
    for evp in burst_noburst:
        bday = burst[evp[0]].dropna().index.values
        bday = [str(x).split('T')[0].replace("-","") for x in bday]
        eday = get_eday(evp)
        if len(set(bday) & set(eday)) != 0:
            anddays = list(set(bday) & set(eday))
            days = []
            for andday in anddays:
                if cnt_logs(evp[1],andday):
                    days.append(andday)
                else:
                    continue
            result.append((evp,days))

    with open('partial_burst','wb') as f:
        pickle.dump(result,f)

    conn.close()
    exit()
