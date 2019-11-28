"""
    Copyright (c) 2019 SuperSonic(https://randychen.tk)
    
    Copyright (c) 2019 Star Inc. (https://starinc.xyz)
    The file modified from Star Python MDS Technology
    under Mozilla Public License v2.0

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

# Initializing
import json

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler

switch_data = {}
auth_code = 0


# Functions
def mds_exit(null=None, null_=None):
    exit(0)


def update(path, data):
    global switch_data
    try:
        if type(path) is list:
            over = query(path)
            over.get("data").update(data)
            return {"status" : 200}
        return {"status" : 400}
    except:
        return {"status": 500}


def delete(path, data):
    global switch_data
    try:
        if type(path) is list:
            over = query(path)
            over.get("data").pop(data)
            return {"status": 200}
        return {"status": 400}
    except:
        return {"status": 500}


def query(query_data, null=None):
    global switch_data
    try:
        if type(switch_data) is dict and type(query_data) is list:
            result = switch_data
            query_len = len(query_data) - 1
            for count, key in enumerate(query_data):
                if key in result:
                    if count < query_len:
                        if type(result.get(key)) is not dict:
                            result = 1 #"unknown_type" + type(source_data.get(key))
                            break
                    result = result.get(key)
                else:
                    result = 2 #"unknown_key"
                    break

            return {"status": 200, "data": result}
        return {"status": 400}
    except:
        return {"status": 500}


def sync(path, null=None):
    global switch_data
    try:
        switch_data = path
        return {"status": 200}
    except:
        return {"status": 500}


# Works
_work = {
    "EXT": mds_exit,
    "UPT": update,
    "DEL": delete,
    "GET": query,
    "SYC": sync,
}


class IndexHandler(RequestHandler):
    def get(self):
        self.write('''
            <b>PBP API Server</b><br>
            The security project for Internet.<hr>
            (c)2019 <a href="https://randychen.tk">SuperSonic</a>.
        ''')

    def post(self):
        global auth_code
        req_body = self.request.body
        req_str = req_body.decode('utf8')
        req_res = json.loads(req_str)
        if req_res.get("code") == auth_code:
            result = _work[req_res.get("do")](req_res.get("path"), req_res.get("data"))
        else:
            result = {"status" : 401}
        if not result:
            result = {"status" : 500}
        self.write(json.dumps(result))


# Main
def listen(code):
    global auth_code
    auth_code = code
    app = Application([('/',IndexHandler)])
    server = HTTPServer(app)
    server.listen(2020)
    IOLoop.current().start()
