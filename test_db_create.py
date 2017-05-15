#!/usr/bin/python
# coding: UTF-8

import sys
import sqlite3
import time
import re
import os.path
import tqdm
import random
import tqdm

'''
syth testdata

24h, 30 - 1,500 count
'''

PARSE_CHAR = ['(',')','[',']','=']
DBNAME = 'test.db'

#word split by space and parse char
def word_split(log):
    w = list(log)
    for (i,word) in enumerate(w):
        if word in PARSE_CHAR:
            w[i] = ' ' + w[i] + ' '
    w = ''.join(w)
    w = re.split(' +',w)
    if w[-1] == '':
        w = w[:-1]
    return w[MSG_OFFSET:]

#get format from db
#return: ft = [[group id, format]]
def get_ft():
    dbname = sys.argv[1]
    con = sqlite3.connect(dbname)
    cur = con.cursor()
    cur.execute("""select * from format""")
    data = cur.fetchall()
    data = [ [data[i][0],data[i][1].strip() ] for i in range(len(data)) ]
    con.commit()
    con.close()
    return data

#compare format and log
#return: 0 -> match, other -> not match
def compare_f(log,fmt):
    l = word_split(log)
    f = fmt.split()
    if len(l) != len(f):#まず長さで評価
        return 1
    flag = 0
    for (lw,fw) in zip(l,f):
        if fw == '*':
            continue
        elif lw != fw:
            flag +=1
    return flag

#get time stamp(sec) from log
def get_time_sec(log):
    time_stamp = log.split()[TIME_OFFSET].split(':')
    time_sec = int(time_stamp[0])*60*60+int(time_stamp[1])*60+int(time_stamp[2])
    return time_sec

def sec2time(sec):
    return str(int(sec/3600)).zfill(2)+':'+str(int(sec%3600/60)).zfill(2)+':'+str(int(sec%3600%60)).zfill(2)

def insert_db(ind,msg,time_sec):
    con = sqlite3.connect(DBNAME)
    cur = con.cursor()

    cur.execute("""drop table if exists '{0}' """.format(ind))
    cur.execute("""create table if not exists '{0}' (id integer primary key,time integer,log text)""".format(ind))
    cur.execute("""insert into format(id,f) values ({0},'{1}');""".format(ind,msg))

    for time_stamp in time_sec:
        cur.execute("""insert into '{0}'(time,log) values ({1},'{2}');""".format(ind,time_stamp,msg))
    con.commit()
    con.close()


if __name__ == '__main__':

    #initialize
    con = sqlite3.connect(DBNAME)
    cur = con.cursor()
    cur.execute("""drop table if exists format """)
    cur.execute("""create table if not exists format(id integer,f text)""")
    con.commit()
    con.close()

    #group_log_list: {group id : log}
    # group_log_list = {k:[] for k in range(1,20)}

    ind = 1

    start_time = random.randint(0,60*60*24 - 60*5)
    msg = 'Burst: 5min({0}-{1}) 1000cnt burst points'.format(sec2time(start_time),sec2time(start_time+60*5))
    time_sec = []
    for i in range(1000):
        time_sec.append(random.randint(start_time,start_time+60*5))
    time_sec = sorted(time_sec)
    insert_db(ind,msg,time_sec)
    ind += 1


    '''
    msg = 'Period: 5min period'
    time_sec = [x * 60 * 5 for x in range( int( 60*60*24 / (60*5) ) ) ]
    insert_db(ind,msg,time_sec)
    ind += 1

    msg = 'Period: 10min period'
    time_sec = [x * 60 * 10 for x in range( int( 60*60*24 / (60*10) ) ) ]
    insert_db(ind,msg,time_sec)
    ind += 1

    msg = 'Period: 15min period'
    time_sec = [x * 60 * 15 for x in range( int( 60*60*24 / (60*15) ) ) ]
    insert_db(ind,msg,time_sec)
    ind += 1

    msg = 'Period: 20min period'
    time_sec = [x * 60 * 20 for x in range( int( 60*60*24 / (60*20) ) ) ]
    insert_db(ind,msg,time_sec)
    ind += 1

    msg = 'Period: 30min period'
    time_sec = [x * 60 * 30 for x in range( int( 60*60*24 / (60*30) ) ) ]
    insert_db(ind,msg,time_sec)
    ind += 1

    msg = 'Period: 7min period'
    time_sec = [x * 60 * 7 for x in range( int( 60*60*24 / (60*7) ) ) ]
    insert_db(ind,msg,time_sec)
    ind += 1
    '''

    # msg = 'Period: 5min period with some irregular point'
    # time_sec = [x * 60 * 60 for x in range( int( 60*60*24 / (60*60) ) ) ]
    # # for i in range(30):
    # #     time_sec[random.randint(0,len(time_sec)-1)] += 2
    # insert_db(ind,msg,time_sec)
    # ind += 1

    '''
    msg = 'Period: 30min period with some irregular point'
    time_sec = [x * 60 * 30 for x in range( int( 60*60*24 / (60*30) ) ) ]
    for i in range(5):
        time_sec[random.randint(0,len(time_sec)-1)] += 2
    insert_db(ind,msg,time_sec)
    ind += 1

    msg = 'Period: 60min period with some irregular point'
    time_sec = [x * 60 * 60 for x in range( int( 60*60*24 / (60*60) ) ) ]
    for i in range(3):
        time_sec[random.randint(0,len(time_sec)-1)] += 2
    insert_db(ind,msg,time_sec)
    ind += 1

    start_time = random.randint(0,60*60*24 - 60*5)
    msg = 'Burst: 5min({0}-{1}) 1000cnt burst points'.format(sec2time(start_time),sec2time(start_time+60*5))
    time_sec = []
    for i in range(1000):
        time_sec.append(random.randint(start_time,start_time+60*5))
    time_sec = sorted(time_sec)
    insert_db(ind,msg,time_sec)
    ind += 1

    start_time = random.randint(0,60*60*24 - 60*10)
    change_time = start_time + int(60*8)
    msg = 'Burst: 10min({0}-{1}) 1000cnt burst points with trend change {2}'.format(sec2time(start_time),sec2time(start_time+60*10),sec2time(change_time))
    time_sec = []
    for i in range(1000):
        time_sec.append(random.randint(start_time,change_time))
    for i in range(4000):
        time_sec.append(random.randint(change_time,start_time+60*10))
    time_sec = sorted(time_sec)
    insert_db(ind,msg,time_sec)
    ind += 1

    start_time = random.randint(0,60*60*24 - 60*10)
    msg = 'Random: 10 / 1h'
    time_sec = []
    for i in range(24):
        for j in range(10):
            time_sec.append(random.randint(i*60*60,(i+1)*60*60))
    time_sec = sorted(time_sec)
    insert_db(ind,msg,time_sec)
    ind += 1

    start_time = random.randint(0,60*60*24 - 60*5)
    msg = 'Period Burst: 10min period with one burst point 5min({0}-{1})'.format(sec2time(start_time),sec2time(start_time+60*5))
    time_sec = [x * 60 * 10 for x in range( int( 60*60*24 / (60*10) ) ) ]
    for i in range(1000):
        time_sec.append(random.randint(start_time,start_time+60*5))
    time_sec = sorted(time_sec)
    insert_db(ind,msg,time_sec)
    ind += 1

    start_time1 = random.randint(0,60*60*24 - 60*5)
    start_time2 = random.randint(0,60*60*24 - 60*5)
    start_time3 = random.randint(0,60*60*24 - 60*5)
    msg = 'Period Burst: 10min period with 3 burst points 5min({0}-{1},{2}-{3},{4}-{5})'.format(sec2time(start_time1),sec2time(start_time1+60*5),sec2time(start_time2),sec2time(start_time2+60*5),sec2time(start_time3),sec2time(start_time3+60*5))
    time_sec = [x * 60 * 10 for x in range( int( 60*60*24 / (60*10) ) ) ]
    for i in range(1000):
        time_sec.append(random.randint(start_time1,start_time1+60*5))
        time_sec.append(random.randint(start_time2,start_time2+60*5))
        time_sec.append(random.randint(start_time3,start_time3+60*5))
    time_sec = sorted(time_sec)
    insert_db(ind,msg,time_sec)
    ind += 1


    start_time = random.randint(0,60*60)
    msg = 'Period Burst: 10min period with 30min period burst points 5min({0}-{1})'.format(sec2time(start_time1),sec2time(start_time1+60*5))
    time_sec = [x * 60 * 10 for x in range( int( 60*60*24 / (60*10) ) ) ]
    for _ in range(int((60*60*24-start_time)/(60*30))):
        for i in range(1000):
            time_sec.append(random.randint(start_time,start_time+60*5))
        start_time += 60*30
    time_sec = sorted(time_sec)
    insert_db(ind,msg,time_sec)
    ind += 1
    '''
    #
    # while(ind<10):
    #     start_time1 = random.randint(0,60*60*24 - 60*10)
    #     start_time2 = random.randint(0,60*60*24 - 60*10)
    #     start_time3 = random.randint(0,60*60*24 - 60*10)
    #     msg = 'Random Burst: 100 / 1h with 3 burst point 5min({0}-{1},{2}-{3},{4}-{5})'.format(sec2time(start_time1),sec2time(start_time1+60*10),sec2time(start_time2),sec2time(start_time2+60*10),sec2time(start_time3),sec2time(start_time3+60*10))
    #     time_sec =   []
    #     for i in range(24):
    #         for j in range(100):
    #             time_sec.append(random.randint(i*60*60,(i+1)*60*60-1))
    #     for i in range(1000):
    #         time_sec.append(random.randint(start_time1,start_time1+60*10))
    #     for i in range(1000):
    #         time_sec.append(random.randint(start_time2,start_time2+60*10))
    #     for i in range(1000):
    #         time_sec.append(random.randint(start_time3,start_time3+60*10))
    #     time_sec = sorted(time_sec)
    #     insert_db(ind,msg,time_sec)
    #     ind += 1

    '''

    msg = 'Period: 60min period with a lack point'
    time_sec = [x * 60 * 60 for x in range( int( 60*60*24 / (60*60) ) ) ]
    del(time_sec[random.randint(0,len(time_sec)-1)])
    insert_db(ind,msg,time_sec)
    ind += 1


    start_time1 = random.randint(0,60*60*24 - 60*10)
    start_time2 = random.randint(0,60*60*24 - 60*10)
    start_time3 = random.randint(0,60*60*24 - 60*10)
    msg = 'Burst: 10min burst with 3 different size burst points 5min({0}-{1},{2}-{3},{4}-{5})'.format(sec2time(start_time1),sec2time(start_time1+60*10),sec2time(start_time2),sec2time(start_time2+60*10),sec2time(start_time3),sec2time(start_time3+60*10))
    time_sec = []
    for i in range(2000):
        time_sec.append(random.randint(start_time1,start_time1+60*10))
    for i in range(2000):
        time_sec.append(random.randint(start_time2,start_time2+60*10))
    for i in range(2000):
        time_sec.append(random.randint(start_time3,start_time3+60*10))
    time_sec = sorted(time_sec)
    insert_db(ind,msg,time_sec)
    ind += 1
    '''

    '''
    1	2	3	5
    100	500	1000	2000	3000
    1min	3min	5min	10min
    '''
    #
    # #回数(3)、サイズ(3000)、期間(5)をランダムに
    # # counts = [1,2,3,5]
    # # sizes = [100,500,1000,2000,3000]
    # # lengths = [1,3,5,10]
    # counts = [1,2,3]
    # denses = [0.1,1.0,10,100]
    # lengths = [10,60,120,180]
    #
    #
    # for count in counts:
    #     for dens in denses:
    #         for length in lengths:
    #             cur = 0
    #             while(True):
    #                 # start_time = [random.randint(0,60*60*24 - 60*length) for _ in range(10)]
    #                 start_time = [72000,43200,14400]
    #                 time_sec = []
    #                 for i in range(count):
    #                     for _ in range(int(dens*length)):
    #                         time_sec.append(random.randint(start_time[i],start_time[i]+60*length))
    #
    #                 for i in range(24):
    #                     for _ in range(4):
    #                         time_sec.append(random.randint(i*60*60,(i+1)*60*60-1))
    #
    #                 time_sec = sorted(time_sec)
    #                 msg = 'Burst: cnt {0} '.format(count)
    #                 for i in range(count):
    #                     msg += 'length {0} dens {1} ({2}-{3}) '.format(length,dens,sec2time(start_time[i]),sec2time(start_time[i]+60*length))
    #                 insert_db(ind,msg,time_sec)
    #                 ind += 1
    #                 cur += 1
    #                 print(ind)
    #                 if cur == 10:
    #                     break

    #回数(1,2,3,5)、密度(100,500,1000,2000,3000)、期間(1,3,5,10)を全パターン10回ずつ,with random
    # counts = [1,2,3]
    # denses = [0.1,1.0,10,100]
    # lengths = [10,60,120,180]
    # random_rates = [100]
    # random_rates = [1,3,10]
    counts = [1]
    denses = [100]
    lengths = [180]
    random_rates = [0]

    for random_rate in random_rates:
        for count in counts:
            for dens in denses:
                for length in lengths:
                    cur = 0
                    while(True):
                        start_time = [72000,43200,14400]
                        time_sec = []

                        for i in range(count):
                            for _ in range(int(dens*length)):
                                time_sec.append(random.randint(start_time[i],start_time[i]+60*length))

                        for i in range(24):
                            for j in range(random_rate):
                                time_sec.append(random.randint(i*60*60,(i+1)*60*60-1))

                        # time_sec.append(1258)
                        #
                        # for i in range(1,15):
                        #     time_sec.append(1258+5053*i)

                        time_sec = sorted(time_sec)

                        msg = 'Burst: {0} random {1} '.format(count,random_rate)
                        for i in range(count):
                            msg += 'length {0} dens {1} ({2}-{3})'.format(length,dens,sec2time(start_time[i]),sec2time(start_time[i]+60*length))
                        insert_db(ind,msg,time_sec)

                        ind += 1
                        cur += 1
                        print(count)
                        # if cur == 10:
                        if cur == 1:
                            break

    # #回数(1,2,3,5)、密度(100,500,1000,2000,3000)、期間(1,3,5,10)を全パターン10回ずつwith period
    # counts = [1,2,3]
    # denses = [0.1,1.0,10,100]
    # lengths = [10,60,120,180]
    # periods = [3,5,10,30,60,120]
    # for count in counts:
    #     for dens in denses:
    #         for length in lengths:
    #             for period in periods:
    #                 cur = 0
    #                 while(True):
    #                     # if count >= 2 and lengths == 480:
    #                     #     break
    #
    #                     start_time = [72000,43200,14400]
    #
    #                     if period != 0:
    #                         time_sec = [x * 60 * period for x in range( int( 60*60*24 / (60*period) ) ) ]
    #                     else:
    #                         time_sec = []
    #
    #                     for i in range(count):
    #                         for _ in range(int(dens*length)):
    #                             time_sec.append(random.randint(start_time[i],start_time[i]+60*length))
    #
    #                     time_sec = sorted(time_sec)
    #
    #                     msg = 'Burst: {0} period {1} '.format(count,period)
    #                     for i in range(count):
    #                         msg += '{0} min, dens {1} ({2}-{3}) '.format(length,dens,sec2time(start_time[i]),sec2time(start_time[i]+60*length))
    #                     insert_db(ind,msg,time_sec)
    #                     ind += 1
    #                     cur += 1
    #                     print(ind)
    #                     if cur == 10:
    #                         break


    # #周期(3-70min),irregular point(全体の20%以下、+-3秒)
    # periods = [3,5,7,10,15,30,60,90]
    # # irregular_rates = [0.0,0.1,0.2,0.3,0.4,0.5]
    # noizes = [0.0,0.1,0.3,0.5,0.8]
    # for period in periods:
    #     for noize in noizes:
    #         count = 0
    #         while(count < 100):
    #             # irregular_cnt = int(60*24/period*irregular_rate)
    #             time_sec = [x * 60 * period for x in range( int( 60*60*24 / (60*period) ) ) ]
    #             # for i in range(irregular_cnt):
    #             #     d = random.randint(0,1)
    #             #     if d == 0:
    #             #         d = -1
    #             #     irregular_time = random.randint(0,len(time_sec)-1)
    #             #     time_sec[irregular_time] += d*random.randint(1,3)
    #
    #             all_cnt = 24*60/period
    #             noize_cnt = all_cnt / (1 - noize) * noize
    #
    #             for _ in range(int(noize_cnt)):
    #                 time_sec.append(random.randint(0,24*60*60-1))
    #             sorted(time_sec)
    #             msg = 'Period: {0} min ({1} sec) period with {2} % noize'.format(period,period*60,noize*100)
    #             insert_db(ind,msg,time_sec)
    #             ind += 1
    #             count += 1
    #

    # while(ind<(7*3)):
    #     #周期(3-70min),irregular point(全体の20%以下、+-5秒),3/1hのノイズ
    #     for period in [3,5,7,10,15,30,60]:
    #         irregular_cnt = random.randint(1,int(60*24/period/5))
    #         time_sec = [x * 60 * period for x in range(1, int( 60*60*24 / (60*period) ) ) ]
    #
    #         for i in range(24):
    #             for j in range(3):
    #                 time_sec.append(random.randint(i*60*60,(i+1)*60*60-1))
    #
    #         for i in range(irregular_cnt):
    #             d = [-1,1][random.randint(0,1)]
    #             time_sec[random.randint(0,len(time_sec)-1)] += d*random.randint(1,5)
    #
    #         msg = 'Period: {0} min ({4} sec) period with {1} irregular point ( {1} / {2} = {3} % ) with 1/h noizes'.format(period,irregular_cnt,60*24/period,round(irregular_cnt/(60*24/period)*100,1),period*60)
    #         # msg = 'Period: {0} min ({1} sec) with 5 / 1h random noizes'.format(period,period*60)
    #         insert_db(ind,msg,time_sec)
    #         ind += 1


    # #random log 3min or 5min
    # while(ind<50):
    #     interval = [3,5,5,5,5,5,2]
    #     time_sec = [0]
    #     cur = 0
    #     while( cur < (60*60*24 - 60*5) ):
    #         cur += interval[random.randint(0,6)]*60
    #         time_sec.append(cur)
    #     msg = 'Random: 3min or 5min interval'
    #     insert_db(ind,msg,time_sec)
    #     ind += 1

    # #random log
    # random_rates = [1,3,10,100,1000]
    # for random_rate in random_rates:
    #   while(True):
    #     time_sec = []
    #     for i in range(24):
    #         for _ in range(random_rate):
    #             time_sec.append(random.randint(i*60*60,(i+1)*60*60-1))
    #     msg = 'Random: random log {0} cnt/min'.format(random_rate)
    #     insert_db(ind,msg,time_sec)
    #     ind += 1
    #     if (ind-1)%10 == 0:
    #         break


    # msg = 'Period: 3min 3min 5min repeat'
    # period = [3,6,11]
    # time_sec = [ x * 60 * 11 + period[y%3]*60 for x in range( int(60*24 / 11) * 3 ) for y in range(3) if x * 60 * 11 < 86400 - 11 * 60]
    # insert_db(ind,msg,time_sec)
    # ind += 1

    # #周期(30min),irregular point(全体の20%以下、+-3秒),間に5分間隔を忍ばせる
    # while(ind < 10):
    #     period = random.randint(30,30)
    #     irregular_cnt = random.randint(1,int(60*24/period/5))
    #     time_sec = [x * 60 * period for x in range( int( 60*60*24 / (60*period) ) ) ]
    #
    #     for i in range(irregular_cnt):
    #         d = random.randint(0,1)
    #         if d == 0:
    #             d = -1
    #         irregular_time = random.randint(0,len(time_sec)-1)
    #         time_sec[irregular_time] += d*random.randint(1,3)
    #
    #     for _ in range(8):
    #         i = random.randint(0,23)
    #         j = random.randint(30,60*60-900)
    #         time_sec.append(i*60*60 + j)
    #         time_sec.append(i*60*60 + j + 180 * 1)
    #         time_sec.append(i*60*60 + j + 180 * 2)
    #         time_sec.append(i*60*60 + j + 180 * 3)
    #         time_sec.append(i*60*60 + j + 180 * 4)
    #         time_sec.append(i*60*60 + j + 180 * 5)
    #
    #
    #     msg = 'Period: {0} min ({4} sec) period with {1} irregular point ( {1} / {2} = {3} %)'.format(period,irregular_cnt,60*24/period,round(irregular_cnt/(60*24/period)*100,1),period*60)
    #     time_sec = sorted(time_sec)
    #     insert_db(ind,msg,time_sec)
    #     ind += 1


    exit()
    #予備datファイル生成
    outputname = sys.argv[1].split('.')[0]+'.dat'
    fd = open(outputname,"w")

    for k in range(1,ft[-1][0]+1):
        fd.write('group {0}\n'.format(k))
        for log in group_log_list[k]:
            fd.write(log)
            fd.write('\n')

    fd.close()
