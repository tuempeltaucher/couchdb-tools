#!/usr/bin/env python
import sys, os
import couchdb
import time
import json

if not len(sys.argv) == 3:
    print "$ http://localhost:5984/db dump_dir"
    sys.exit(1)

uri = sys.argv[1]
dump_dir = sys.argv[2]

if not os.path.exists(dump_dir):
    print "%s does not exist" % (dump_dir)
    sys.exit(1)

db = couchdb.Db(uri)

for f in os.listdir(dump_dir):
    doc_id = f.replace("#", "/")
    print doc_id
    with open(dump_dir + "/" + f, "rb") as fp:
        db.delete("/" + doc_id)
        data = json.loads(fp.read())
        del data["_rev"]
        db.put("/" + doc_id, json.dumps(data))
