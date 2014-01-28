#!/usr/bin/env python
import sys, os
import couchdb
import time

if len(sys.argv) < 3:
    print "$ dump_dir http://localhost:5984/db [design]"
    sys.exit(1)

dump_dir = sys.argv[1]
uri = sys.argv[2]

db = couchdb.Db(uri)

if len(sys.argv) > 3 and sys.argv[3] == "design":
    docids = db.fetch_all_design()
else:
    docids = db.fetch_all()

n = 0
for id in docids:
    fname = dump_dir + "/" + id.replace("/", "#")
    data = db.get("/" + id)
    with open(fname, "wb") as fp:
        fp.write(data)
        n += 1

print "saved %i documents into %s" % (n, dump_dir)
