import sqlite3
import numpy as np
import pandas as pd

if __name__ == "__main__":
    with open("rp_edge_result",'r') as f:
        line=[i.strip() for i in f.readlines()]
        # event_df = pd.DataFrame(columns=['srcID','srcHost','dstID','dstHost','direction','date'])
        # date_df = pd.DataFrame(columns=['edgeID','date'])

        lt_df = pd.DataFrame(columns=['ltid','lt'])
        i = 0
        # line = all_data

        while i<len(line):
            # if 'term' in line[i]:
                # date = line[i].split()[2]
            # elif 'undirected' in line[i]:
                # direc = 0
            # elif 'directed' in line[i]:
                # direc = 1
            if 'src>' in line[i]:
                ltID = line[i].split()[2]
                i+=1
                lt = line[i]
                if ltID in lt_df['ltid']:
                    if lt_df[lt_df['ltid'] == ltID]['lt'] != lt:
                        print('error');exit()
                else:
                    lt_df = lt_df.append(pd.Series([ltID,lt],index=lt_df.columns),ignore_index=True)
            elif 'dst>' in line[i]:
                ltID = line[i].split()[2]
                i+=1
                lt = line[i]
                # print(lt_df['ltid'].values)
                # print('10' in lt_df['ltid'].values);exit()
                if ltID in lt_df['ltid'].values:
                    # print(lt_df,'\n',ltID,lt_df[lt_df['ltid'] == ltID]['lt'].values == lt);exit()
                    if (lt_df[lt_df['ltid'] == ltID]['lt'].values != lt)[0]:
                        print('error');exit()
                else:
                    lt_df = lt_df.append(pd.Series([ltID,lt],index=lt_df.columns),ignore_index=True)
            i+=1


        # dbname = 's4causality.db'
        # conn = sqlite3.connect(dbname)
        # cur = conn.cursor()
        #
        # cur.execute('''create table lt (ltID int, lt txt)''')
        # for row in lt_df.ix[:,:5].drop_duplicates().iterrows():
        #     cur.execute('''insert into event(srcID, srcHost, dstID, dstHost, direction) values({0[0]},"{0[1]}",{0[2]},"{0[3]}",{0[4]})'''.format(row[1].values[:5]))
        #
        # conn.commit()
        # conn.close()
