import pickle
import datetime
import sys
import glob
import collections
import pandas as pd
import numpy as np


'''
hostの全集計dfのdump生成

python host_pandas.py prefix

* prefix/0000-0499

'''

PREFIX = sys.argv[1]

def print_full(x):
    pd.set_option('display.max_rows', len(x))
    pd.set_option('display.max_columns', len(x.columns))
    print(x)
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')


# files = glob.glob('dump_files/0000-0499/*_tokyo-dc-rm.dump') # ワイルドカードが使用可能
files = glob.glob('{0}/*-*/*'.format(PREFIX)) # ワイルドカードが使用可能

host_list = []
for fi in files:
    host_list.append(fi.split('/')[-1].split('.')[0].split('_')[1])


for host in set(host_list):

    # パス内の全ての"指定パス+ファイル名"と"指定パス+ディレクトリ名"を要素とするリストを返す
    files = glob.glob('{0}/*-*/*_{1}.dump'.format(PREFIX,host)) # ワイルドカードが使用可能


    df_tmp = pd.DataFrame(index=pd.date_range('20120101','20130331'), columns=np.arange(1789))

    for fi in files:
        tmp_id = int(fi.split('/')[-1].split('_')[0])

        with open(fi,"rb") as f:
            obj = pickle.load(f, encoding="bytes")

        tmp = set( [datetime.datetime(row.year,row.month,row.day) for row in obj ] )
        x = sorted(list(tmp))

        # Y軸データ
        y = sorted(collections.Counter([row.date() for row in obj]).items(),key=lambda x:x[0])
        y = [row[1] for row in y]

        for ind,val in zip(x,y):
            df_tmp.loc[ind,tmp_id] = val

    with open(host + '_df.dump','wb') as f:
        pickle.dump(df_tmp,f)
