from spango.service.servers.http.request import HttpRequest
from spango.service.servers.http.response import HttpResponse
from spango.service.servers.http import core
from spango.service.variable import Variable


class HttpServer:

    @classmethod
    def __init__(cls, ss):
        cls.ss = ss
        # 处理请求响应
        cls.execute()

    @classmethod
    def execute(cls):
        try:
            # 创建变量类
            cls.variable = Variable()
            # 创建request
            cls.request = HttpRequest()
            # 创建response
            cls.response = HttpResponse()

            # 接收响应数据
            core.loop_data(cls.ss, cls.request, cls.response, cls.variable)
        except Exception as e:
            # print('--error--:', e)
            raise e
