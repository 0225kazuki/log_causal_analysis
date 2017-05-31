import pickle
import datetime
import sys
import glob
import search_burst as sb

'''
event別dumpファイルをhostごとに集約
python event_agg.py prefix

prefix以下が、
prefix/0000-0499/hoge.dump

'''


days = [i.split('/')[-1] for i in glob.glob('dumps/*')]

for day in days:
    hosts = set([i.split('_')[-1] for i in glob.glob('dumps/{0}/*'.format(day))])
    for host in hosts:
        files = glob.glob('dumps/{0}/*_{1}'.format(day,host))
        host_data = []
        for fi in files:
            host_data.extend(sb.open_dump(fi))

        with open('dumps_host/{0}/{1}'.format(day,day+'_'+host),'wb') as f:
            pickle.dump(host_data,f)

# # files = glob.glob('dump_files/0000-0499/*_tokyo-dc-rm.dump') # ワイルドカードが使用可能
# files = glob.glob('{0}/*-*/*'.format(PREFIX)) # ワイルドカードが使用可能
#
# host_list = []
# for fi in files:
#     host_list.append(fi.split('/')[-1].split('.')[0].split('_')[1])
#
# print(set(host_list),len(set(host_list)))
# #
# # with open("host_list.txt","w") as f:
# #     for i in set(host_list):
# #         f.write(str(i))
# #         f.write("\n")
# #
# # exit()
#
#
# for host in set(host_list):
#
#     # パス内の全ての"指定パス+ファイル名"と"指定パス+ディレクトリ名"を要素とするリストを返す
#     files = glob.glob('{0}/*-*/*_{1}.dump'.format(PREFIX,host)) # ワイルドカードが使用可能
#
#     all_event = []
#
#     for fi in files:
#         with open(fi,"rb") as f:
#             obj = pickle.load(f, encoding="bytes")
#
#         # all_num += len(obj)
#         all_event.extend(obj)
#
#     with open(host + '.dump','wb') as f:
#         pickle.dump(all_event,f)
