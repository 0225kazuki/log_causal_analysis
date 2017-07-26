import pickle
import datetime
import sys
import glob
import collections
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
# import search_burst as sb

def open_dump(dump_file):
    with open(dump_file,"rb") as f:
        obj = pickle.load(f, encoding="bytes")
    return obj

def get_ids(host,get_date):
    # 特定日の特定ホストのIDを全部取得
    ids = []
    for i in glob.glob('dumps/{0}/*_{1}'.format(get_date,host)):
        ids.append((i.split("/")[-1].split("_")[0],len(open_dump(i))))

    sorted(ids,key=lambda x:x[1],reverse=True)
    return ids


if __name__ == "__main__":

    get_dates = [i.split('/')[-1] for i in glob.glob('dumps_host/*')]

    colors = ['red','orange','y','lightgreen','green','lightblue','blue','purple','gray','black']

    bursts = open_dump('burst_df')

    dump_result = []

    # 全日付で回す
    for get_date in get_dates:
        print(get_date)

        # 日付に該当する全ホストで回す
        for host in [i.split('/')[-1].split('_')[-1] for i in glob.glob('dumps_host/{0}/*'.format(get_date))]:
            # 日付，ホストに該当するIDを全部取得
            ids = get_ids(host,get_date)

            # 特定日の特定ホストベースでバーストが検知されてたら
            if len(open_dump('burst_result_host/{0}/{1}'.format(get_date,get_date+'_'+host)))==3:
                filename, filedatem, h_burst = open_dump('burst_result_host/{0}/{1}'.format(get_date,get_date+'_'+host))

                # ホストのバーストのst，en
                h_st_ens = [(i[1],i[2]) for i in h_burst]

                # 全部のIDのバーストのst,enを取得
                st_ens = []
                for id_,c in ids:
                    bs = bursts[str(id_)+'_'+host][get_date]
                    if type(bs) == list:
                        for b in bs:
                            st_ens.append((b[1],b[2]))

                # ホストのバーストに対してデバイスのバースト期間と被りがあるものは除外
                result = []
                for h_st,h_en in h_st_ens:
                    flag=0
                    for st,en in st_ens:
                        if h_st <= en and h_en >= st:#かぶりがあるなら
                            flag=1
                            break
                    if flag == 0 :#被りがなかったら残す
                        result.append((h_st,h_en))

                # 日付とホストごとに残ったバーストを記録
                if result != []:
                    dump_result.append((host,get_date,result))

    # dump
    with open('host_burst_df','wb') as f:
        pickle.dump(dump_result,f)
