import pickle
import datetime
import sys
import glob
import collections
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import host_plot_day


'''

dict = {event:value}
value = {date : time}

'''



def burst2get_data(burst_file):
    # print(burst_file)
    get_data = collections.defaultdict(lambda: 0)
    for line in open(burst_file,"r"):
        if line[0] == '(':
            get_date = "".join([a.strip().zfill(2) for a in line[1:-2].split(",")])
            get_data[get_date] = []
        elif line.strip()[0] == "[":
            st = line.strip()[1:-2].split(",")[1].strip()
            en = line.strip()[1:-2].split(",")[2].strip()
            get_data[get_date].append((float(st),float(en)))

    return get_data

def create_burst_dict(pf):
    files = glob.glob('{0}/*-*/*'.format(pf))
    columns = [fi.split("/")[-1].split(".dump.txt")[0] for fi in files]
    burst_df = pd.DataFrame(index=pd.date_range('20120101','20130331'), columns=columns)
    for fi,col in zip(files,columns):
        event_name = fi.split('/')[-1].split('.')[0]
        get_data = burst2get_data(fi)
        if len(get_data) == 0:
            continue
        else:
            # burst_dict[event_name] = get_data
            for d,v in get_data.items():
                d = pd.to_datetime(d)
                # print(type(d))
                burst_df.loc[d,col] = v
                print(burst_df.loc[d])

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
    PREFIX = sys.argv[1]


    burst_df = create_burst_dict(PREFIX)

    with open('burst_df','wb') as f:
        pickle.dump(burst_df,f)


    # search_day(burst_dict)
