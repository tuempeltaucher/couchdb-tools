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

    def create_request(self, method, uri):
        request = urllib2.Request(uri)
        request.get_method = lambda: method
        request.add_header("Content-Type", "application/json")
        if not self.username == None:
            base64string = base64.encodestring('%s:%s' % (self.username, self.password)).replace('\n', '')
            request.add_header("Authorization", "Basic %s" % base64string)
        return request

    def get_request(self, method, path):
        return self.create_request(method, self.uri + path)

    def getraw(self, path):
        request = self.get_request("GET", path)
        res = urllib2.urlopen(request)
        return res.read()

    def putraw(self, path, data):
        request = self.get_request("PUT", path)
        urllib2.urlopen(request, data)

    def put(self, path, data):
        self.putraw(path, json.dumps(data))

    def delete(self, path):
        doc = None
        try:
            doc = self.getraw(path)
        except:
            pass
        if doc:
            j = json.loads(doc)
            request = self.get_request("DELETE", path + "?rev=" + j["_rev"])
            urllib2.urlopen(request)

    def fetch_all(self):
        l = json.loads(self.getraw("/_all_docs"))
        for r in l["rows"]:
            yield r["id"]

    def fetch_all_design(self):
        l = json.loads(self.getraw("/_all_docs?startkey=\"_design/\"&endkey=\"_design0\""))
        for r in l["rows"]:
            yield r["id"]

    def exists(self, path="/"):
        try:
            self.getraw(path)
            return True
        except:
            return False

    def create(self):
        if not self.exists():
            request = self.get_request("PUT", "/")
            urllib2.urlopen(request)

    def add_user(self, username, password):
        p = self.uri.find("://")
        uri = self.uri[0:self.uri.find("/", p+3)]
        id = "org.couchdb.user:" + username

        req = self.create_request("GET", uri + "/_users/" + id)
        try:
            urllib2.urlopen(req)
            return True
        except:
            pass

        data = dict()
        data["_id"] = id
        data["name"] = username
        data["type"] = "user"
        data["roles"] = []
        data["password"] = password

        req = self.create_request("PUT", uri + "/_users/" + id)
        urllib2.urlopen(req, json.dumps(data))

        return True

    def set_dbperm(self, username):
        data = {
            "admins": {
                "names": [],
                "roles": ["_admin"],
            },
            "readers": {
                "names": [username],
                "roles": []
            }
        }
        self.put("/_security", data)
