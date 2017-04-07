import pickle
import sqlite3
import datetime
import sys

DUMP_FILE = sys.argv[1]

with open(DUMP_FILE) as f:
    obj = pickle.load(f)


for evdef, times in obj.items():
    event_name = str(evdef.gid) + '_' + evdef.host
    print(event_name)
    with open(event_name+'.dump','wb') as f:
        pickle.dump(times,f)
