#  控制变量容器
# variable container


class Variable:
    http_connection = 'close'
    request_method = None

    def set_initialize(self):
        self.http_connection = 'close'
        self.request_method = None
