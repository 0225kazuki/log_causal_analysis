import collections
import pprint
import re
import sys
import time
import numpy as np
import pybursts
import math
from concurrent import futures
from itertools import chain
import pickle
import datetime
import burst_detect_all as bd



def open_dump(dump_file):
    with open(dump_file, "rb") as f:
        obj = pickle.load(f, encoding="bytes")
    return obj


def burst_detect_from_dump(DUMP_NAME):
    try:
        obj = open_dump(DUMP_NAME)
    except:
        print("Input should be dump path");exit()

    time_list = sorted([x.hour*3600 + x.minute*60 + x.second for x in obj])

    # cur_t = -1
    #
    # for i, t in enumerate(time_list):
    #     if cur_t == t:
    #         time_list[i] = round(time_list[i-1]+0.01, 3)
    #     else:
    #         cur_t = t

    cur_t = time_list[0]
    for i, t in enumerate(time_list[1:]):
        if cur_t == t:
            time_list[i] = round(time_list[i-1]+0.01, 3)
        else:
            cur_t = t



    time_lists = {1:time_list}

    print(time_lists)

    return bd.burst_detect(time_lists)


if __name__ == "__main__":
    print(burst_detect_from_dump(sys.argv[1]))
