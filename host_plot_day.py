import pickle
import datetime
import sys
import glob
import collections
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


'''
特定の日の、ID別プロット

no option:
python host_plot_day.py tokyo-dc-rm_df.dump 20120101 prefix

./prefix/0000-0499/イベント別データ
のファイル構造から、自動で、入力日の上位10件の発生イベントを拾ってきてプロットする

option: a
python host_plot_day.py a tokyo-dc-rm_df.dump burst_result prefix"

burst_resultからバーストが検知された日を抽出し、
./prefix/0000-0499/イベント別データ
のファイル構造から、自動で、入力日の上位10件の発生イベントを拾ってきて、全日プロットする

'''


def create_xy(dump_name,get_date):
    #特定日の累積和プロット用の階段処理してあるx, yを生成
    obj = open_dump(dump_name)

    plot_year = int(get_date[:4])
    plot_month = int(get_date[4:6])
    plot_day = int(get_date[6:8])

    plot_date = datetime.date(plot_year,plot_month,plot_day)

    plot_data = [row.time() for row in obj if row.date() == plot_date]

    plot_data_coll = collections.Counter(plot_data)

    x = [row.hour*3600 + row.minute*60 + row.second for row in sorted(set(plot_data))]
    y = [0]
    for row in sorted(plot_data_coll.items(),key=lambda z:z[0]):
        y.append(row[1]+y[-1])
    y = y[1:]

    x = np.sort(np.append(x,x))[1:]
    x = np.insert(x,0,x[0])

    tmp = []
    for row in y:
        tmp.append(row)
        tmp.append(row)

    y = tmp[:-1]
    y = [0] + y

    if x[-1] != 86399:
        x = np.append(x,86399)
        y = np.append(y,y[-1])

    return (x,y)

def print_full(x):
    pd.set_option('display.max_rows', len(x))
    pd.set_option('display.max_columns', len(x.columns))
    print(x)
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')

def open_dump(dump_file):
    with open(dump_file,"rb") as f:
        obj = pickle.load(f, encoding="bytes")
    return obj

def get_most_ids(df,get_date):
    #dfから特定日の大量発生しているIDを降順に取得 -> ids
    id_sr = df.loc[get_date]
    # id_sr.sort(ascending=False)
    id_sr = id_sr.sort_values(inplace=False, ascending=False)
    id_sr = id_sr.dropna()

    ids = id_sr.index

    print(id_sr)
    return ids

def burst2get_dates(burst_file):
    get_dates = []
    for line in open(burst_file,"r"):
        if line[0] == '(':
            get_date = "".join([a.strip().zfill(2) for a in line[1:-2].split(",")])
            get_dates.append(get_date)
        else:
            continue

    return get_dates

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage:\npython host_plot_day.py tokyo-dc-rm_df.dump 20120101 prefix")
        print("python host_plot_day.py a tokyo-dc-rm_df.dump burst_result.txt prefix")
        exit()

    if sys.argv[1] == 'a':
        dump_name = sys.argv[2]
        burst_file = sys.argv[3]
        prefix = sys.argv[4]

        get_dates = burst2get_dates(burst_file)
    else:
        dump_name = sys.argv[1]
        get_dates = [sys.argv[2]]
        prefix = sys.argv[3]



    colors = ['red','orange','y','lightgreen','green','lightblue','blue','purple','gray','black']

    df = open_dump(dump_name)
    host_name = dump_name.split("/")[-1].split('_')[0]

    print(host_name)
    print(get_dates)


    for get_date in get_dates:
        ids = get_most_ids(df,get_date)

        # データをセット
        fig = plt.figure(figsize=(30,10))
        #default left : 0.125　right : 0.9　bottom : 0.1　top : 0.9　wspace : 0.2　hspace : 0.2
        fig.subplots_adjust(left=0.03,right=0.999)

        for cnt,idd in enumerate(ids):
            if cnt > 9:
                break

            id_host = str(idd) + '_' + host_name + '.dump'

            if idd < 500:
                id_host_path = prefix + "/0000-0499/" + id_host
            elif idd < 1000:
                id_host_path = prefix + "/0500-0999/" + id_host
            elif idd < 1500:
                id_host_path = prefix + "/1000-1499/" + id_host
            else:
                id_host_path = prefix + "/1500-1999/" + id_host

            x,y = create_xy(id_host_path,get_date)
            print(idd,y[-1])

            plt.plot(x, y,label=idd,color=colors[cnt], lw='3')


        #総計データのプロット
        x, y = create_xy("host_dump/"+host_name+".dump",get_date)
        plt.plot(x, y, "--", label='all', color="black", lw='3')


        plt.xticks([i*3600 for i in range(25)],[str(i).zfill(2)+':00\n{0}'.format(i*3600) for i in range(25)],rotation=90)
        plt.xlim(0,86400)
        plt.grid()
        plt.legend()

        # plt.savefig(DUMP_NAME.split('/')[-1].split('.')[0]+'_'+DATE+'.png')
        plt.savefig(host_name + get_date + '.png')
