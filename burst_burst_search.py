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
burst - burstを探す
edge-coburstのevpairに対して，
ev1とev2共にバーストが起きている日(共起かは見ていない) & エッジが引かれた日
を出している。
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

            result.append((evp,anddays))

    with open('burst_burst_all','wb') as f:
        pickle.dump(result,f)

    conn.close()
    exit()
