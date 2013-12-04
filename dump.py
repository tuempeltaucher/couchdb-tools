#!/usr/bin/env python
import sys, os
import couchdb
import time

if not len(sys.argv) == 2:
    print "$ http://localhost:5984/db"
    sys.exit(1)

uri = sys.argv[1]

dump_dir = "./dump-%s" % (time.time())
os.mkdir(dump_dir)

db = couchdb.Db(uri)

n = 0
for id in db.fetch_all():
    fname = dump_dir + "/" + id.replace("/", "#")
    data = db.get("/" + id)
    with open(fname, "wb") as fp:
        fp.write(data)
        n += 1

print "saved %i documents into %s" % (n, dump_dir)
