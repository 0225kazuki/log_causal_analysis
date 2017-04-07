import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
import sys
import datetime
import collections

values = []
dn_list = []

for dn in sys.argv[1:]:
    DUMP_NAME = dn
    dn_list.append(dn.split('/')[-1])

    with open(DUMP_NAME,"rb") as f:
        obj = pickle.load(f, encoding="bytes")

    tmp = set( [datetime.datetime(row.year,row.month,row.day) for row in obj ] )
    x = sorted(list(tmp))

    print(dn,'\t',x[0],x[-1])
