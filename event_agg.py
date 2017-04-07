import pickle
import sqlite3
import datetime
import sys
import glob

'''
event別dumpファイルをhostごとに集約
'''

# files = glob.glob('dump_files/0000-0499/*_tokyo-dc-rm.dump') # ワイルドカードが使用可能
files = glob.glob('dump_files/*-*/*') # ワイルドカードが使用可能

host_list = []
for fi in files:
    host_list.append(fi.split('/')[-1].split('.')[0].split('_')[1])

print(set(host_list),len(set(host_list)))
#
# with open("host_list.txt","w") as f:
#     for i in set(host_list):
#         f.write(str(i))
#         f.write("\n")
#
# exit()


for host in set(host_list):

    # パス内の全ての"指定パス+ファイル名"と"指定パス+ディレクトリ名"を要素とするリストを返す
    files = glob.glob('dump_files/*-*/*_{0}.dump'.format(host)) # ワイルドカードが使用可能

    all_event = []

    for fi in files:
        with open(fi,"rb") as f:
            obj = pickle.load(f, encoding="bytes")

        # all_num += len(obj)
        all_event.extend(obj)

    with open(host + '.dump','wb') as f:
        pickle.dump(all_event,f)
