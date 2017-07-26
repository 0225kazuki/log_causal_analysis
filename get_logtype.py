# args: conf, ltgid
import sys
from logcausality import log_db
from logcausality import lt_label

conf = sys.argv[0]
ltgid = sys.argv[1]

ld = log_db.LogData(conf)
ll = lt_label.init_ltlabel(conf)
label = ll.get_ltg_label(ltgid, ld.ltg_members(ltgid))
group = ll.get_group(label)
print(group)
