from spango.service.developer.http import Request
from spango.service.servers.http import core
from spango.service.servers.http.request import HttpRequest
from spango.service.servers.http.response import HttpResponse
from spango.service.variable import Variable


class HttpServer:

    @classmethod
    def __init__(cls, ss):
        cls.ss = ss
        # 处理请求响应
        cls.execute()
        # 关闭流
        if cls.variable.http_connection == 'close':
            cls.ss.close()

    @classmethod
    def execute(cls):
        try:
            # 定义变量类
            cls.variable = Variable()
            # 定义request
            cls.request = Request(HttpRequest())
            # 定义response
            cls.response = HttpResponse()
            # 接收响应数据
            core.loop_data(cls.ss, cls.request, cls.response, cls.variable)
            # # 接收数据
            # core.receive_data(cls.ss, cls.request)
            # # 处理数据
            # cls.processing_data()
            # # 响应数据
            # core.send_data(cls.ss, cls.response)

        except Exception as e:
            # print('--error--:', e)
            raise e

    # # 处理数据
    # @classmethod
    # def processing_data(cls):
    #     # 获取目录信息
    #     rootPath = Constant.ROOT_PATH
    #     static_path = Constant.STATIC_PATH
    #     templates_path = Constant.TEMPLATES_PATH
    #
    #     print("收到请求头：", cls.request.headers)
    #     if cls.request.headers.get('Connection'):
    #         cls.variable.http_connection = cls.request.headers.get('Connection')
    #     try:
    #         if cls.request.body:
    #             print("收到请求体：", cls.request.body.decode(Constant.DECODE))
    #     except UnicodeDecodeError:
    #         print("收到请求体：", cls.request.body)
    #     print("收到FormData：", cls.request.data_block)
    #
    #     print("接收的url：", cls.request.url)
    #     print("收到查询字符串：", cls.request.search_str)
    #     print("接收单个参数abc", cls.request.get('abc'))
    #     aaa = cls.request.gets('abc')
    #     print("接收数组参数abc", aaa)
    #
    #     # url长度限制校验
    #     if cls.request.url is None or len(cls.request.url) > Constant.maxUrlSize:
    #         cls.response.set_status('400')
    #         return
    #
    #     regex = UrlList.matching(cls.request.url)
    #     print('匹配到：', regex)
    #     if regex is None:
    #         # 匹配静态资源
    #         if cls.request.url.find('?') != -1:
    #             filename = static_path + cls.request.url[:cls.request.url.find('?')]
    #         else:
    #             filename = static_path + cls.request.url
    #         content = cls.read_file(filename)
    #         if content:
    #             cls.response.content = content
    #         else:
    #             # 返回404
    #             cls.response.set_status('404', url=cls.request.url)
    #
    #         return
    #
    #     if isinstance(regex.get('view'), str):
    #         filename = templates_path + regex.get('view')
    #         content = cls.read_file(filename)
    #         cls.response.content = content
    #     elif isfunction(regex.get('view')):
    #         print(222222222222222222)
    #     else:
    #         print('无法处理的url')

        # 优先匹配urls列表中的内容，如匹配不到，则匹配static目录
        ##########返回给客户端
        # print(11111111, type(static_path))
        # print(22222222, type(cls.request.url))
        # static_file = static_path + cls.request.url
        ##########返回给客户端
        # end

    # # 读取文件资源
    # @classmethod
    # def read_file(cls, filename):
    #     if os.path.isfile(filename):
    #         content = bytes()
    #         with open(filename, "rb") as f:
    #             for line in f:
    #                 content += line
    #             f.close()
    #         return content
