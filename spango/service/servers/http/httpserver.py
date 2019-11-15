import os

from inspect import isfunction
from spango.urls.url_list import UrlList
from spango.service.constant import Constant
from spango.service.servers.http import core
from spango.service.servers.http.request import Request
from spango.service.servers.http.response import Response

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = curPath[:curPath.find('spango')]
static_path = rootPath + 'static/'
templates_path = rootPath + 'templates/'


class HttpServer:

    @classmethod
    def __init__(cls, ss):
        cls.ss = ss
        # 处理请求响应
        cls.execute()

    @classmethod
    def execute(cls):
        try:
            # 定义request
            cls.request = Request()
            # 定义response
            cls.response = Response()
            # 接收数据
            core.receive_data(cls.ss, cls.request)
            # 处理数据
            cls.processing_data()
            # 响应数据

        except Exception as e:
            # print('--error--:', e)
            raise e

    # 处理数据
    @classmethod
    def processing_data(cls):
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
        regex = UrlList.matching(cls.request.url)
        print('匹配到：', regex)
        if isinstance(regex.get('view'), str):
            print(111111111111111111)
            filename = templates_path + regex.get('view')
            content = cls.read_file(filename)
            cls.response.content = content
        elif isfunction(regex.get('view')):
            print(222222222222222222)
        else:
            print('无法处理的url')

        # 优先匹配urls列表中的内容，如匹配不到，则匹配static目录
        ##########返回给客户端
        static_file = static_path + cls.request.url
        ##########返回给客户端
        # end

    # 读取文件资源
    @classmethod
    def read_file(cls, filename):
        content = bytes()
        with open(filename, "rb") as f:
            for line in f:
                content += line
            f.close()
        return content
