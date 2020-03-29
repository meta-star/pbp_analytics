import json
from abc import ABC

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler
from tornado.websocket import WebSocketHandler

"""
    Copyright (c) 2019 SuperSonic(https://randychen.tk)

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

response_handle = ()

hello_msg = '''
<b>PBP API Server</b>
<br>The security project for Internet.
<hr>(c)2020 <a href="https://github.com/supersonictw">SuperSonic</a>.
'''


class HttpHandler(RequestHandler, ABC):
    """
    
    """

    async def get(self):
        self.write(hello_msg)
        await self.finish()

    async def post(self):
        req_body = self.request.body
        req_str = req_body.decode('utf8')
        try:
            req_res = json.loads(req_str)
        except json.decoder.JSONDecodeError:
            req_res = {}
        if req_res.get("version") is not None:
            result = {"status": 500}
            if response_handle:
                for handle in response_handle:
                    result = await handle(req_res)
        else:
            if req_res:
                result = {"status": 400}
            else:
                result = {"status": 401}
        self.write(json.dumps(result))
        await self.finish()


class WSHandler(WebSocketHandler, ABC):
    """

    """

    def check_origin(self, origin):
        return True

    def open(self):
        self.write_message(json.dumps({
            "status": 200,
            "msg": hello_msg
        }))

    async def on_message(self, message):
        try:
            req_res = json.loads(message)
        except json.decoder.JSONDecodeError:
            req_res = {}
        if req_res.get("version") is not None:
            result = {"status": 500}
            if response_handle:
                for handle in response_handle:
                    result = await handle(req_res)
        else:
            if req_res:
                result = {"status": 400}
            else:
                result = {"status": 401}
        await self.write_message(json.dumps(result))

    def on_close(self):
        pass


class WebServer:
    """

    """

    def __init__(self, pbp_handle):
        global response_handle
        response_handle = (pbp_handle.server_response,)
        pbp_handle.get_time()

    @staticmethod
    def listen():
        """

        :return:
        """
        app = Application([
            ('/', HttpHandler),
            ('/ws', WSHandler)
        ])
        server = HTTPServer(app)
        server.listen(2020)
        IOLoop.current().start()
