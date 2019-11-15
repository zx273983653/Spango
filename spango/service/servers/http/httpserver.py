import os

from urllib import parse
from spango.service.constant import Constant
from spango.service import initaction
from spango.service.servers.http.request import Request
from spango.service.servers.http.response import Response

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = curPath[:curPath.find('spango/service/servers')]
static_path = rootPath + 'static'


class HttpServer:

    @classmethod
    def __init__(cls, ss):
        cls.ss = ss
        # 初始化配置信息
        initaction.action()
        # 处理请求响应
        cls.execute()
        # 结束后执行

    @classmethod
    def execute(cls):
        try:
            cls.receive_data()
        except Exception as e:
            # print('--error--:', e)
            raise e
        print("收到请求头：", cls.request.headers)
        try:
            print("收到请求体：", cls.request.body.decode(Constant.DECODE))
        except UnicodeDecodeError:
            print("收到请求体：", cls.request.body)
        print("收到FormData：", cls.request.data_block)

        print("接收的url：", cls.request.url)
        print("收到查询字符串：", cls.request.search_str)
        print("接收单个参数abc", cls.request.get('abc'))
        aaa = cls.request.gets('abc')
        print("接收数组参数abc", aaa)

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
            cls.request.content += tmp_data
            if cls.request.content.find(b'\r\n\r\n') != -1:
                proto_data = cls.request.content[:cls.request.content.find(b'\r\n')]
                header_data = cls.request.content[cls.request.content.find(b'\r\n') + 2:cls.request.content.find(b'\r\n\r\n')]

                # 封装请求头
                header_lines = header_data.split(b'\r\n')
                for header_line in header_lines:
                    tmp_key = header_line.split(b': ')[0]
                    tmp_value = header_line.split(b': ')[1]
                    cls.request.headers[tmp_key.decode(Constant.DECODE)] = tmp_value.decode(Constant.DECODE)

                # 封装url
                cls.request.url = proto_data[proto_data.find(b' ') + 1:proto_data.find(b' HTTP/')].decode(Constant.DECODE)

                # 封装查询字符串
                if cls.request.url.find('?') != -1:
                    cls.request.search_str = cls.request.url[cls.request.url.find('?') + 1:]

                # 封装请求方式
                if proto_data.startswith(b'GET'):
                    cls.request.method = "GET"
                    break
                elif proto_data.startswith(b'POST'):
                    cls.request.method = "POST"

                    # 封装请求体
                    len_body = cls.request.headers.get('Content-Length')
                    if len_body:
                        cls.request.body = cls.request.content[cls.request.content.find(b'\r\n\r\n') + 4:]
                        break
                    else:
                        break

                elif proto_data.startswith(b'HEAD'):
                    cls.request.method = "HEAD"
                else:
                    print('__error__:目前不支持该请求方式')
                    break

        # 处理form-data发包方式
        if cls.request.headers.get('Content-Type') and cls.request.headers.get('Content-Type').find('multipart/form-data') != -1:
            if cls.request.body:
                boundary = cls.request.body[:cls.request.body.find(b'\r\n')]
                data_blocks = cls.request.body.split(boundary)
                for data_block in data_blocks:
                    if data_block.find(b'\r\n\r\n') != -1:
                        one_line = data_block[data_block.find(b'\r\n') + 2:data_block.find(b'\r\n\r\n')]
                        one_lines = one_line.split(b'\r\n')
                        data_block_dict = {}
                        for tmp_line in one_lines:
                            if tmp_line.find(b';') != -1:
                                tmp_lines2 = tmp_line.split(b';')
                                for tmp_line2 in tmp_lines2:
                                    if tmp_line2.find(b' name=') != -1:
                                        data_name = tmp_line2[tmp_line2.find(b' name="') + 7:-1].decode(
                                            Constant.DECODE)
                                        data_block_dict['data_name'] = data_name
                                    if tmp_line2.find(b' filename=') != -1:
                                        filename = tmp_line2[
                                                   tmp_line2.find(b' filename="') + 11:-1].decode(
                                            Constant.DECODE)
                                        data_block_dict['filename'] = filename
                                    if tmp_line2.find(b'Content-Type:') != -1:
                                        content_type = tmp_line2[
                                                       tmp_line2.find(b'Content-Type:') + 13:].decode(
                                            Constant.DECODE)
                                        data_block_dict['content_type'] = content_type
                        data_value = data_block[data_block.find(b'\r\n\r\n') + 4:-2]

                        try:
                            data_block_dict['data_value'] = data_value.decode(Constant.DECODE)
                        except UnicodeDecodeError:
                            data_block_dict['data_value'] = data_value
                        cls.request.data_block.append(data_block_dict)
