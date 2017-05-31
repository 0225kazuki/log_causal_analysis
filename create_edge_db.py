import sqlite3
import numpy as np
import pandas as pd

if __name__ == "__main__":
    with open("rp_edge_result",'r') as f:
        all_data=[i.strip() for i in f.readlines()]
        event_df = pd.DataFrame(columns=['srcID','srcHost','dstID','dstHost','direction','date'])
        date_df = pd.DataFrame(columns=['edgeID','date'])
        lt_df = pd.DataFrame(columns=['ltid','lt'])
        i = 0
        line = all_data

        while i<len(all_data):
            if 'term' in line[i]:
                date = line[i].split()[2]
            elif 'undirected' in line[i]:
                direc = 0
            elif 'directed' in line[i]:
                direc = 1
            elif 'src>' in line[i]:
                srcID = line[i].split()[2]
                srcHost = line[i].split()[6][:-1]
            elif 'dst>' in line[i]:
                dstID = line[i].split()[2]
                dstHost = line[i].split()[6][:-1]
                event_df = event_df.append(pd.Series([srcID,srcHost,dstID,dstHost,direc,date],index=event_df.columns),ignore_index=True)
            i+=1

        dbname = 's4causality.db'
        conn = sqlite3.connect(dbname)
        cur = conn.cursor()

        cur.execute('''create table event (pairID integer primary key, srcID int, srcHost txt, dstID int, dstHost txt, direction int)''')
        for row in event_df.ix[:,:5].drop_duplicates().iterrows():
            cur.execute('''insert into event(srcID, srcHost, dstID, dstHost, direction) values({0[0]},"{0[1]}",{0[2]},"{0[3]}",{0[4]})'''.format(row[1].values[:5]))

        cur.execute('''create table date (id integer primary key, pairID integer, date text)''')
        for row in event_df.iterrows():
            cur.execute('''select pairID from event where srcID={0[0]} and srcHost="{0[1]}" and dstID={0[2]} and dstHost="{0[3]}" and direction={0[4]}'''.format(row[1].values[:5]))
            pairID = cur.fetchall()[0][0]
            cur.execute('''insert into date(pairID, date) values({0},"{1}")'''.format(pairID, row[1].values[-1]))

        conn.commit()
        conn.close()
