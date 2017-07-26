#!/usr/bin/python

import numpy as np
import pandas as pd
import datetime
import search_burst as sb
import plot_day
import pickle
import search_burst as sb
import sqlite3
import collections

'''
相似形のものかどうか判別
'''

def cnt_logs(DUMP_NAME,DATE):
    obj = sb.open_dump('dumps/'+str(DATE)+'/'+DUMP_NAME)
    return(len(obj))


def get_eday(evp):
    argv = []
    argv.extend(evp[0].split("_"))
    argv.extend(evp[1].split("_"))
    query='select date from date where pairID in(select pairID from event where (srcID={0} and srcHost="{1}" and dstID={2} and dstHost="{3}") or (srcID={2} and srcHost="{3}" and dstID={0} and dstHost="{1}"));'.format(argv[0],argv[1],argv[2],argv[3])
    cur.execute(query)
    r  = cur.fetchall()
    result = []
    for i in r:
        result.append("".join(i[0].split("-")))
    return result


def get_log(DUMP_NAME,DATE):
    obj = sb.open_dump('dumps/'+str(DATE)+'/'+DUMP_NAME)
    return(obj)


def check_synm(evp,anddays):
    res1 = []
    res2 = []
    for day in anddays:
        ev1 = get_log(evp[0],day)
        lev1 = len(ev1)
        ev2 = get_log(evp[1],day)
        lev2 = len(ev2)

        ev1 = collections.Counter([i.strftime('%H%M') for i in ev1])
        # lev1 = ev1.most_common(1)[0][1]
        ev2 = collections.Counter([i.strftime('%H%M') for i in ev2])
        # lev2 = ev2.most_common(1)[0][1]

        ev1s = {k:int(v/lev1*100) for k,v in ev1.items()}
        ev2s = {k:int(v/lev2*100) for k,v in ev2.items()}
        # print(ev1s);exit()
        if evp[0] == '117_tokyo-dc-rm' and evp[1] == '116_tokyo-dc-rm':
            print(ev1,ev2)
            print(ev1s,ev2s)

        res1.append(ev1==ev2)
        res2.append(ev1s==ev2s)

    return any(res1),any(res2)


if __name__ == "__main__":

    dbname = 's4causality.db'
    conn  = sqlite3.connect(dbname)
    cur = conn.cursor()

    edge_burst = sb.open_dump('rp_edge_coburst')

    print(len(edge_burst))

    burst = sb.open_dump('burst_df')
    burst_ev = [x for x in burst.columns if len(burst[x].dropna()) != 0]

    result = []
    for evp in edge_burst['EvPair']:
        bday1 = burst[evp[0]].dropna().index.values
        bday1 = [str(x).split('T')[0].replace("-","") for x in bday1]
        bday2 = burst[evp[1]].dropna().index.values
        bday2 = [str(x).split('T')[0].replace("-","") for x in bday2]
        bday = list(set(bday1) & set(bday2))
        eday = get_eday(evp)
        if len(set(bday) & set(eday)) != 0:
            anddays = list(set(bday) & set(eday))
            res1,res2 = check_synm(evp,anddays)
            result.append((evp,anddays,res1,res2))

    # print(result)


    with open('burst_burst_synm_min','wb') as f:
        pickle.dump(result,f)


    conn.close()
    exit()
