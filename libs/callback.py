import json
from abc import ABC

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler
from tornado.websocket import WebSocketHandler

"""
    Copyright (c) 2020 Star Inc.(https://starinc.xyz)

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
    Http Handle
    ---
    Default URL:
        http://localhost:2020/
    """

    async def get(self):
        self.write(hello_msg)
        await self.finish()

    async def post(self):
        req_body = self.request.body
        req_str = req_body.decode('utf8')
        result = {"status": 202}
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
        global response_handle
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
