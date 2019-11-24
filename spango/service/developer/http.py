# 提供给开发者调用
from multidict import CIMultiDict


class Request:
    # 请求的原始数据
    content = None
    # 状态行
    status_line = None
    # 请求头
    headers = CIMultiDict()
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
        self.status_line = http_request.status_line
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

    def get_cookies(self):
        c = {}
        cookies = self.headers.get('Cookie')
        if cookies:
            blocks = cookies.split('; ')
            for block in blocks:
                kvs = block.split('=')
                if len(kvs) == 2:
                    k = kvs[0]
                    v = kvs[1]
                    c[k] = v
        return c


class Response:
    # 状态码
    status_code = None
    # 状态行
    status_line = None
    # 响应头
    headers = None
    # 响应体
    body = None
    # 响应体原始数据
    content = None
    # 最终响应的全部内容
    data = None

    def __init__(self, http_response):
        self.http_response = http_response
        self.status_code = http_response.status_code
        self.status_line = http_response.status_line
        self.headers = http_response.headers
        self.body = http_response.body
        self.content = http_response.content
        self.data = http_response.data
        self.variable = http_response.variable

    # 设置状态码
    def set_status(self, code, **kwargs):
        self.http_response.set_status(code, **kwargs)

    # 重定向
    def redirect(self, url):
        self.status_code = '302'
        self.status_line = 'HTTP/1.1 302 Found'
        self.headers['location'] = url

    # 设置cookie
    def set_cookie(self, cookies, path='/', domain=None):
        cookie_list = []
        for k in cookies.keys():
            if domain:
                cookie_value = "%s=%s; path=%s; domain=%s" % (k, cookies[k], path, domain)
            else:
                cookie_value = "%s=%s; path=%s" % (k, cookies[k], path)
            cookie_list.append(cookie_value)
        self.headers['Set-Cookie'] = cookie_list
