import json
from abc import ABC

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler

"""
    Copyright (c) 2019 SuperSonic(https://randychen.tk)

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""


def analytics_func(data):
    return {"status": -1, "reply": data}


class IndexHandler(RequestHandler, ABC):
    def get(self):
        self.write('''
            <b>PBP API Server</b><br>
            The security project for Internet.<hr>
            (c)2020 <a href="https://github.com/supersonictw">SuperSonic</a>.
        ''')

    def post(self):
        req_body = self.request.body
        req_str = req_body.decode('utf8')
        req_res = json.loads(req_str)
        if req_res.get("version") is not None:
            result = analytics_func(req_res)
        else:
            result = {"status": 400}
        self.write(json.dumps(result))


class HttpServer:
    def __init__(self, pbp_handle):
        global analytics_func
        analytics_func = pbp_handle.analytics
        pbp_handle.get_time()

    @staticmethod
    def listen():
        app = Application([
            ('/', IndexHandler)
        ])
        server = HTTPServer(app)
        server.listen(2020)
        IOLoop.current().start()
