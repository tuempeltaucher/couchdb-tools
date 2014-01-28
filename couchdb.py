import json
import os
import urllib2
import base64
import json

class Db():
    username = None
    password = None

    def __init__(self, uri):
        if "@" in uri and ":" in uri:
            p = uri.find("://")+3
            self.username = uri[p:uri.find(":", p)]
            self.password = uri[uri.find(":", p)+1:uri.find("@")]
            uri = uri[0:p] + uri[uri.find("@")+1:]
        self.uri = uri
        if self.username == None:
            self.load_netrc()

    def load_netrc(self):
        f = os.path.expanduser("~") + "/.netrc"
        if os.path.exists(f):
            with open(f, "r") as fp:
                line = fp.readline()

                p = line.find("login ") + len("login ")
                p1 = line.find(" ", p)
                self.username = line[p:p1]

                p = line.find("password ") + len("password ")
                self.password = line[p:].strip()

    def get_request(self, method, path):
        request = urllib2.Request(self.uri + path)
        request.get_method = lambda: method
        request.add_header("Content-Type", "application/json")
        if not self.username == None:
            base64string = base64.encodestring('%s:%s' % (self.username, self.password)).replace('\n', '')
            request.add_header("Authorization", "Basic %s" % base64string)
        return request

    def get(self, path):
        request = self.get_request("GET", path)
        res = urllib2.urlopen(request)
        return res.read()

    def put(self, path, data):
        request = self.get_request("PUT", path)
        urllib2.urlopen(request, data)

    def delete(self, path):
        doc = None
        try:
            doc = self.get(path)
        except:
            pass
        if doc:
            j = json.loads(doc)
            request = self.get_request("DELETE", path + "?rev=" + j["_rev"])
            urllib2.urlopen(request)

    def fetch_all(self):
        l = json.loads(self.get("/_all_docs"))
        for r in l["rows"]:
            yield r["id"]

    def fetch_all_design(self):
        l = json.loads(self.get("/_all_docs?startkey=\"_design/\"&endkey=\"_design0\""))
        for r in l["rows"]:
            yield r["id"]

