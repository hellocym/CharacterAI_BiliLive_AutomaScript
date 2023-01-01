# -*- coding:utf-8 -*-

from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib
import json

import requests


last_message = None


def get_message():
    global last_message
    url = "http://api.live.bilibili.com/ajax/msg?roomid="
    room = "114514"
    res = requests.get(url+room).json()
    res = res['data']['room'][-1]
    if res == last_message:
        return None
    else:
        last_message = res
        return res


'''========【http端口服务】========'''


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path, args = urllib.parse.splitquery(self.path)
        # self._response(path, args)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        if message := get_message():
            data = {'result': message['text'], 'status': 0}
            self.wfile.write(json.dumps(data).encode())
        else :
            data = {'result': '', 'status': -1}
            self.wfile.write(json.dumps(data).encode())

    def do_POST(self):
        args = self.rfile.read(int(self.headers['content-length'])).decode("utf-8")
        print(args)
        self._response(self.path, args)

    def _response(self, path, args):
        # 组装参数为字典
        if args:
            args = urllib.parse.parse_qs(args).items()
            args = dict([(k, v[0]) for k, v in args])
        else:
            args = {}
        # 设置响应结果
        result = {"status": 0, "msg": "操作成功", "data": [{"page_id": 1}, {"page_id": 2}]}
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())


if __name__ == '__main__':
    # 开启http服务，设置监听ip和端口
    httpd = HTTPServer(('', 8787), HttpHandler)
    httpd.serve_forever()
    # 运行后 http://localhost:8787 即可访问该接口
