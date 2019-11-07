import ssl
from urllib import parse
import socks
import socket


class HttpServer:

    @classmethod
    def __init__(cls, ss):
        cls.ss = ss
        cls.execute()

    @classmethod
    def execute(cls):
        cls.receive_data()
        print("收到请求头：", cls.request.headers)
        print("收到请求体：", cls.request.body)

    # 解析url
    @classmethod
    def parse_urls(cls, url):
        proto = 80
        up = parse.urlparse(url)
        if up.scheme != "":
            proto = up.scheme
        dst = up.netloc.split(":")
        if len(dst) == 2:
            port = int(dst[1])
        else:
            if proto == "http":
                port = 80
            elif proto == "https":
                port = 443
        host = dst[0]
        path = up.path
        if path is None or path == '':
            path = '/'
        return proto, host, port, path

    @classmethod
    def receive_data(cls):
        cls.request = Request()
        data = bytes()
        while True:
            tmp_data = cls.ss.recv(1024)
            data += tmp_data
            if data.find('\r\n\r\n') != -1:
                pass


class Request:
    headers = None
    body = None
