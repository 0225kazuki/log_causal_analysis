import sqlite3
import numpy as np
import pandas as pd
import search_burst as sb
import pickle

def search_pair_query(id1,host1,id2,host2):
    query='select date from date where pairID in(select pairID from event where (srcID={0} and srcHost="{1}" and dstID={2} and dstHost="{3}") or (srcID={2} and srcHost="{3}" and dstID={0} and dstHost="{1}"));'.format(id1,host1,id2,host2)
    return query

if __name__ == "__main__":
    co_prob_df = sb.open_dump('co_prob_df')

    dbname = 's4causality.db'
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()

    edge_coburst_pair = []
    for row in co_prob_df['EvPair'].values:
        id1,host1 = row[0].split('_')
        id2,host2 = row[1].split('_')
        q = search_pair_query(id1,host1,id2,host2)
        cur.execute('''{}'''.format(q))
        q_result = cur.fetchall()
        if len(q_result) != 0 :
            edge_coburst_pair.append(row)
        else:
            pass

    edge_coburst_index = pd.Series([False]*co_prob_df.shape[0],index=co_prob_df.index)
    for i in edge_coburst_pair:
        edge_coburst_index |= co_prob_df['EvPair']==i

    with open('rp_edge_coburst','wb') as f:
        pickle.dump(co_prob_df[edge_coburst_index],f)



    # cur.execute('''create table date (id integer primary key, pairID integer, date text)''')
    # for row in event_df.iterrows():
    #     cur.execute('''select pairID from event where srcID={0[0]} and srcHost="{0[1]}" and dstID={0[2]} and dstHost="{0[3]}" and direction={0[4]}'''.format(row[1].values[:5]))
    #     pairID = cur.fetchall()[0][0]
    #     cur.execute('''insert into date(pairID, date) values({0},"{1}")'''.format(pairID, row[1].values[-1]))
    #
    # conn.commit()
    # conn.close()
