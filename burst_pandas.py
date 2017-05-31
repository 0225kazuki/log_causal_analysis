import pickle
import datetime
import sys
import glob
import collections
import pandas as pd
import numpy as np
import search_burst as sb

'''
バースト結果をdfにする
burst_result/*/* -> burst_df[index = date, colmuns = events]
'''

def burst2get_data(burst_file):
    # get_data = collections.defaultdict(lambda: 0)
    get_data = sb.open_dump('burst_file')
    for line in open(burst_file,"r"):
        if line[0] == '(':
            get_date = "".join([a.strip().zfill(2) for a in line[1:-2].split(",")])
            get_data[get_date] = []
        elif line.strip()[0] == "[":
            st = line.strip()[1:-2].split(",")[1].strip()
            en = line.strip()[1:-2].split(",")[2].strip()
            get_data[get_date].append((float(st),float(en)))

    return get_data


def create_burst_df():
    files = glob.glob('burst_result/*/*')
    evs = sorted(list(set(["_".join(fi.split('/')[-1].split("_")[1:]) for fi in files])))

    cols = evs

    burst_df = pd.DataFrame(index=pd.date_range('20120101','20130331'), columns=cols)
    for fi in files:
        event_name = "_".join(fi.split('/')[-1].split('_')[1:])

        print(fi)

        try: # some bursts are detected
            ev,day,data = sb.open_dump(fi)
        except: # no bursts are detected
            continue

        if event_name != ev:
            print('event name error')
            print(event_name,ev,day,data)
            continue
        else:
            d = pd.to_datetime(day)
            burst_df.loc[d,ev] = data

    return burst_df

# def search_day(burst_dict):
#     for date in pd.date_range('20120301','20130331'):
#         date = date.date()
#
#         event_list = []
#         for event in burst_dict:
#             if burst_dict[event][date] != 0:
#                 event_list

if __name__ == "__main__":
    burst_df = create_burst_df()

    with open('burst_df','wb') as f:
        pickle.dump(burst_df,f)

    # search_day(burst_dict)
