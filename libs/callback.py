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


class IndexHandler(RequestHandler, ABC):
    def get(self):
        self.write('''
            <b>PBP API Server</b><br>
            The security project for Internet.<hr>
            (c)2019 <a href="https://randychen.tk">SuperSonic</a>.
        ''')

    def post(self):
        req_body = self.request.body
        req_str = req_body.decode('utf8')
        req_res = json.loads(req_str)
        result = {"status": 401, "reply": req_res}
        self.write(json.dumps(result))


class PBP:
    @staticmethod
    def listen():
        app = Application([
            ('/', IndexHandler)
        ])
        server = HTTPServer(app)
        server.listen(2020)
        IOLoop.current().start()
