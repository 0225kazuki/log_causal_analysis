import sqlite3
import sys


argv = sys.argv[1:]


conn = sqlite3.connect('s4causality.db')
cur = conn.cursor()
query='select date from date where pairID in(select pairID from event where (srcID={0} and srcHost="{1}" and dstID={2} and dstHost="{3}") or (srcID={2} and srcHost="{3}" and dstID={0} and dstHost="{1}"));'.format(argv[0],argv[1],argv[2],argv[3])

cur.execute(query)

for i in cur.fetchall():
    print("".join(i[0].split("-")))


# query='select * from event where (srcID={0} and srcHost="{1}" and dstID={2} and dstHost="{3}") or (srcID={2} and srcHost="{3}" and dstID={0} and dstHost="{1}");'.format(argv[0],argv[1],argv[2],argv[3])
#
# cur.execute(query)
#
# for i in cur.fetchall():
#     print(i)
