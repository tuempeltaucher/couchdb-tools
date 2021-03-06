#!/usr/bin/env python
import sys, os
import couchdb
import time
import json

if len(sys.argv) < 3:
    print "$ http://localhost:5984/db opcode"
    sys.exit(1)

uri = sys.argv[1]
opcode = sys.argv[2]

param1 = None
param2 = None

if len(sys.argv) >= 4:
    param1 = sys.argv[3]
    if len(sys.argv) >= 5:
        param2 = sys.argv[4]

db = couchdb.Db(uri)

if opcode == "create":
    db.create()
elif opcode == "add_user":
    db.add_user(param1, param2)
elif opcode == "set_dbperm":
    db.set_dbperm(param1)
elif opcode == "truncate_data":
    for id in db.fetch_all():
        if id.startswith("_design"):
            continue
        if param1 == None or id.startswith(param1):
            if not param2 == None:
                db.delete("/" + id)
            print "deleted %s" % (id)
else:
    print "invalid opcode"
    sys.exit(1)
