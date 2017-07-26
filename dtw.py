# -*- coding: utf-8 -*-
import numpy as np
import search_burst as sb
import sqlite3
import collections
import datetime
import pickle

def dtw_distance(ts_a, ts_b, d=lambda x, y: abs(x-y), window=0):
    if window <= 0:
        window = max(len(ts_a), len(ts_b))

    ts_a_len = len(ts_a)
    ts_b_len = len(ts_b)

    cost = np.empty((ts_a_len, ts_b_len))
    dist = np.empty((ts_a_len, ts_b_len))

    cost[0][0] = dist[0][0] = d(ts_a[0], ts_b[0])

    for i in range(1, ts_a_len):
        cost[i][0] = d(ts_a[i], ts_b[0])
        dist[i][0] = dist[i-1, 0] + cost[i, 0]

    for j in range(1, ts_b_len):
        cost[0][j] = d(ts_a[0], ts_b[j])
        dist[0][j] = dist[0, j-1] + cost[0, j]

    for i in range(1, ts_a_len):
        windowstart = max(1, i-window)
        windowend = min(ts_b_len, i+window)
        for j in range(windowstart, windowend):
            cost[i][j] = d(ts_a[i], ts_b[j])
            dist[i][j] = min(dist[i-1][j], dist[i][j-1], dist[i-1][j-1]) + cost[i][j]

    return dist[ts_a_len-1][ts_b_len-1]


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


def vect(ev):
    x = [row.hour*3600 + row.minute*60 + row.second for row in sorted(set(ev))]
    y = [0]
    for row in sorted(collections.Counter(ev).items(),key=lambda z:z[0]):
        y.append(row[1]+y[-1])
    y = y[1:]

    return np.array([x,y])


def check_synm(evp,anddays):
    res = []
    for day in anddays:
        ev1 = get_log(evp[0],day)
        lev1 = len(ev1)
        ev2 = get_log(evp[1],day)
        lev2 = len(ev2)

        vev1 = vect(ev1)
        vev2 = vect(ev2)

        if evp[0] == '117_tokyo-dc-rm' and evp[1] == '116_tokyo-dc-rm':
            print(ev1,ev2)

        dtw = dtw_distance(vev1.T, vev2.T, lambda x,y: np.linalg.norm(x/86400.-np.log(y/max(y))) )
        # dtw = dtw_distance(vev1[0],vev2[0])
        res.append((evp,day,dtw))

    return res

if __name__ == "__main__":
    dbname = 's4causality.db'
    conn  = sqlite3.connect(dbname)
    cur = conn.cursor()
    edge_burst = sb.open_dump('rp_edge_coburst')
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
            res = check_synm(evp,anddays)
            result.append(res)

    print(result)
    with open('edge_dtw_xxy','wb') as f:
        pickle.dump(result,f)
