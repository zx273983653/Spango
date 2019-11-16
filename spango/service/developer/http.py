# 提供给开发者调用


class Request:
    # 请求的原始数据
    content = bytes()
    # 请求头
    headers = {}
    # 请求方式
    method = None
    # 请求URL
    url = None
    # 查询字符串
    search_str = None
    # 请求体
    body = None
    # form-data方式时一些参数
    data_block = []

    def __init__(self, http_request):
        self.http_request = http_request
        self.content = http_request.content
        self.headers = http_request.headers
        self.method = http_request.method
        self.url = http_request.url
        self.search_str = http_request.search_str
        self.body = http_request.body
        self.data_block = http_request.data_block

    # 获取参数
    def get(self, param):
        return self.http_request.get(param)

    # 获取集合类型参数
    def gets(self, params):
        return self.http_request.gets(params)


class Response:
    pass
