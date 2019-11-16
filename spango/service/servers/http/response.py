import time
from spango.service.constant import Constant
from spango.service.variable import Variable


class HttpResponse:
    # 状态码
    status_code = None
    # 状态行
    status_line = 'HTTP/1.1 200 OK'
    # 响应头
    headers = {
        "Server": 'Spango/1.0',
        "Date": time.strftime('%a, %d %b %Y %X GMT', time.localtime(time.time())),
        "Content-Type": 'text/html; charset=%s' % Constant.DECODE,
    }
    # 响应体
    body = None
    # 响应体原始数据
    content = bytes()
    # 最终响应的全部内容
    data = bytes()

    def __init__(self, content=None, headers=None, status_line=None, body=None, variable=None):
        if content:
            self.content = content
        if headers:
            self.headers = headers
        if status_line:
            self.status_line = status_line
        if body:
            self.body = body
        if variable:
            self.variable = variable
        else:
            self.variable = Variable()

    # 设置状态码
    def set_status(self, code, **kwargs):
        self.status_code = code
        if code == '404':
            self.status_line = 'HTTP/1.1 404 Not Found'
            if not kwargs.get('page'):
                url = kwargs.get('url')
                page = str()
                page += '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">\r\n'
                page += '<html>\r\n<head><title>404 Not Found</title></head>\r\n'
                page += '<body>\r\n<h1 style="color:#0066CC;">404 Not Found</h1><span style="color:#0066CC;">The requested URL %s was not found on this server.</span>\r\n' % url
                page += '</body>\r\n</html>'
                self.content = page.encode(Constant.DECODE)

        elif code == '400':
            self.status_line = 'HTTP/1.1 400 Bad Url'
            if not kwargs.get('page'):
                url = kwargs.get('url')
                page = str()
                page += '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">\r\n'
                page += '<html>\r\n<head><title>400 Bad Request</title></head>\r\n'
                page += '<body>\r\n<h1 style="color:#0066CC;">400 Bad Request</h1><span style="color:#0066CC;">The requested URL %s was Bad.</span>\r\n' % url
                page += '</body>\r\n</html>'
                self.content = page.encode(Constant.DECODE)

        elif code.startswith('50'):
            self.status_line = 'HTTP/1.1 %s Server Error' % code
            if not kwargs.get('page'):
                url = kwargs.get('url')
                page = str()
                page += '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">\r\n'
                page += '<html>\r\n<head><title>%s Server Error</title></head>\r\n' % code
                page += '<body>\r\n<h1 style="color:#0066CC;">%s Server Error</h1><span style="color:#0066CC;">The requested URL %s encountered a server exception.</span>\r\n' % (code, url)
                error = kwargs.get('error')
                if error:
                    page += '<div style="margin:20px;">%s</div>\r\n' % error
                page += '</body>\r\n</html>'
                self.content = page.encode(Constant.DECODE)

        else:
            self.status_line = 'HTTP/1.1 %s Unknown Status' % code
            if not kwargs.get('page'):
                url = kwargs.get('url')
                page = str()
                page += '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">\r\n'
                page += '<html>\r\n<head><title>%s Unknown Status</title></head>\r\n' % code
                page += '<body>\r\n<h1 style="color:#0066CC;">%s Unknown Status</h1><span style="color:#0066CC;">The requested URL %s encountered a unknown status.</span>\r\n' % (code, url)
                page += '</body>\r\n</html>'
                self.content = page.encode(Constant.DECODE)

    # 封装并返回响应数据
    def setup_data(self):
        # 修改信息
        self.headers['Connection'] = self.variable.http_connection

        # 封装
        self.data += (self.status_line + '\r\n').encode(Constant.DECODE)
        for key in self.headers.keys():
            self.data += ('%s: %s' % (key, self.headers[key]) + '\r\n').encode(Constant.DECODE)
        self.data += '\r\n'.encode(Constant.DECODE)
        self.data += self.content

        return self.data

    # 重定向
    def redirect(self, url):
        print(self.headers)
        print('重定向：', url)
