class Response:
    # 响应的原始数据
    content = bytes()
    # 响应头
    headers = {}

    def __init__(self, content=None, headers=None):
        if not content:
            self.content = content
        if not headers:
            self.headers = headers

    # 重定向
    def redirect(self, url):
        print(self.headers)
        print('重定向：', url)
