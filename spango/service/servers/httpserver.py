import os

from urllib import parse
from spango.service.constant import Constant

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = curPath[:curPath.find('spango\\service\\servers')]
static_path = rootPath + 'static'


class HttpServer:

    @classmethod
    def __init__(cls, ss):
        cls.ss = ss
        cls.execute()

    @classmethod
    def execute(cls):
        try:
            cls.receive_data()
        except Exception as e:
            print(e)
        # print('收到请求方式：', cls.request.method)
        # print('接收全部内容：', cls.request.data)
        print("收到请求头：", cls.request.headers)
        print("收到请求体：", cls.request.body)
        print("接收的url：", cls.request.url)

        # 匹配url
        # 优先匹配urls列表中的内容，如匹配不到，则匹配static目录
        ##########返回给客户端
        static_file = static_path + cls.request.url
        ##########返回给客户端
        # end

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
        while True:
            tmp_data = cls.ss.recv(1024)
            cls.request.data += tmp_data
            if cls.request.data.find(b'\r\n\r\n') != -1:
                proto_data = cls.request.data[:cls.request.data.find(b'\r\n')]
                header_data = cls.request.data[cls.request.data.find(b'\r\n') + 2:cls.request.data.find(b'\r\n\r\n')]

                # 封装请求头
                header_lines = header_data.split(b'\r\n')
                for header_line in header_lines:
                    tmp_key = header_line.split(b': ')[0]
                    tmp_value = header_line.split(b': ')[1]
                    cls.request.headers[tmp_key.decode(Constant.DECODE)] = tmp_value.decode(Constant.DECODE)

                # 封装url
                cls.request.url = proto_data[proto_data.find(b' ') + 1:proto_data.find(b' HTTP/')].decode(Constant.DECODE)

                # 封装请求方式
                if proto_data.startswith(b'GET'):
                    cls.request.method = "GET"
                    break
                elif proto_data.startswith(b'POST'):
                    cls.request.method = "POST"

                    # 封装请求体
                    len_body = cls.request.headers.get('Content-Length')
                    if len_body:
                        cls.request.body = cls.request.data[cls.request.data.find(b'\r\n\r\n') + 4:].decode(Constant.DECODE)
                        break
                    else:
                        break
                else:
                    print('未知请求')
                    break


class Request:
    # 请求的原始数据
    data = bytes()
    # 请求头
    headers = {}
    # 请求方式
    method = None
    # 请求URL
    url = None
    # 请求体
    body = None


class Response:
    # 响应的原始数据
    data = bytes()
    # 响应头
    headers = {}
    # 响应体
    body = None
