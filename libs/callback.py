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

ready = None
ready_pw = None
response_handle = ()

hello_msg = '''
<b>PBP API Server</b>
<br>The security project for Internet.
<hr>(c)2020 <a href="https://github.com/supersonictw">SuperSonic</a>.
'''


class HttpHandler(RequestHandler, ABC):
    """
    Http Handle
    ---
    Default URL:
        http://localhost:2020/
    """

    async def get(self):
        key = self.get_argument('ready_pw', "")
        if key == ready_pw:
            global ready
            ready = True
        self.write(hello_msg)
        await self.finish()

    async def post(self):
        req_body = self.request.body
        req_str = req_body.decode('utf8')
        result = {"status": 202}
        if response_handle and ready:
            for handle in response_handle:
                result = await handle(req_str)
        self.write(json.dumps(result))
        await self.finish()


class WSHandler(WebSocketHandler, ABC):
    """
    WebSocket handle
    ---
    Default URL:
        http://localhost:2020/ws
    """

    def check_origin(self, origin):
        return True

    def open(self):
        self.write_message(json.dumps({
            "status": 201,
            "msg": hello_msg
        }))

    async def on_message(self, message):
        result = {"status": 202}
        if response_handle and ready:
            for handle in response_handle:
                result = await handle(message)
        await self.write_message(json.dumps(result))

    def on_close(self):
        pass


class WebServer:
    """
    Web service of API protocol
    """

    def __init__(self, pbp_handle):
        global response_handle, ready_pw, ready
        ready = pbp_handle.ready
        ready_pw = str(pbp_handle.ready_pw)
        response_handle = (pbp_handle.server_response,)

    @staticmethod
    def listen(port: int):
        """
        Start listen on web services
        :return:
        """
        app = Application([
            ('/', HttpHandler),
            ('/ws', WSHandler)
        ])
        server = HTTPServer(app)
        server.listen(port)
        server.start(0)
        IOLoop.current().start()
