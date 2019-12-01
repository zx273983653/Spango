import time
from spango.service.constant import Constant
from spango.service.variable import Variable


class HttpResponse:
    # 状态码
    status_code = '200'
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
    # 错误信息
    error = None
    # session
    session = None
    # 封装变量容器
    variable = None

    def __init__(self, content=None, headers=None, status_line=None, body=None):
        if content:
            self.content = content
        if headers:
            self.headers = headers
        if status_line:
            self.status_line = status_line
        if body:
            self.body = body

    # 初始化变量
    # initialize
    def set_initialize(self):
        self.status_code = '200'
        self.status_line = 'HTTP/1.1 200 OK'
        self.headers = {
            "Server": 'Spango/1.0',
            "Date": time.strftime('%a, %d %b %Y %X GMT', time.localtime(time.time())),
            "Content-Type": 'text/html; charset=%s' % Constant.DECODE,
        }
        self.body = None
        self.content = bytes()
        self.data = bytes()
        self.error = None
        self.session = None
        self.variable = None

    # 设置状态码
    def set_status(self, code, **kwargs):
        self.status_code = code
        if kwargs.get('line_info'):
            line_info = kwargs.get('line_info')
            self.status_line = 'HTTP/1.1 %s %s' % (code, line_info)
        else:
            line_info = None

        if code == '404':
            if not line_info:
                line_info = 'Not Found'
            self.status_line = 'HTTP/1.1 %s %s' % (code, line_info)

            if not kwargs.get('page'):
                url = kwargs.get('url')
                page = ''
                page += '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">\r\n'
                page += '<html>\r\n<head><title>404 %s</title></head>\r\n' % line_info
                page += '<body>\r\n<h1 style="color:#0066CC;">404 %s</h1><span style="color:#0066CC;">The requested URL %s was not found on this server.</span>\r\n' % (line_info, url)
                page += '</body>\r\n</html>'
                self.content = page.encode(Constant.DECODE)

        elif code == '400':
            if not line_info:
                line_info = 'Bad Url'
            self.status_line = 'HTTP/1.1 %s %s' % (code, line_info)

            if not kwargs.get('page'):
                url = kwargs.get('url')
                page = ''
                page += '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">\r\n'
                page += '<html>\r\n<head><title>400 %s</title></head>\r\n' % line_info
                page += '<body>\r\n<h1 style="color:#0066CC;">400 %s</h1><span style="color:#0066CC;">The requested URL %s was Bad.</span>\r\n' % (line_info, url)
                page += '</body>\r\n</html>'
                self.content = page.encode(Constant.DECODE)

        elif code == '500':
            if not line_info:
                line_info = 'Server Error'
            self.status_line = 'HTTP/1.1 %s %s' % (code, line_info)

            if not kwargs.get('page'):
                url = kwargs.get('url')
                page = ''
                page += '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">\r\n'
                page += '<html>\r\n<head><title>500 %s</title></head>\r\n' % line_info
                page += '<body>\r\n<h1 style="color:#0066CC;">500 %s</h1><span style="color:#0066CC;">The requested URL %s encountered a server exception.</span>\r\n' % (line_info, url)
                error = kwargs.get('error')
                if error:
                    page += '<div style="margin:20px;">%s</div>\r\n' % error
                page += '</body>\r\n</html>'
                self.content = page.encode(Constant.DECODE)
                self.error = error

        elif code.startswith('50'):
            if not line_info:
                line_info = 'Server Error'
            self.status_line = 'HTTP/1.1 %s %s' % (code, line_info)

            if not kwargs.get('page'):
                url = kwargs.get('url')
                page = ''
                page += '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">\r\n'
                page += '<html>\r\n<head><title>%s %s</title></head>\r\n' % (code, line_info)
                page += '<body>\r\n<h1 style="color:#0066CC;">%s %s</h1><span style="color:#0066CC;">The requested URL %s encountered a server exception.</span>\r\n' % (code, line_info, url)
                error = kwargs.get('error')
                if error:
                    page += '<div style="margin:20px;">%s</div>\r\n' % error
                page += '</body>\r\n</html>'
                self.content = page.encode(Constant.DECODE)
                self.error = error

        else:
            if not line_info:
                line_info = 'Unknown Status'
            self.status_line = 'HTTP/1.1 %s %s' % (code, line_info)
            if not kwargs.get('page'):
                url = kwargs.get('url')
                page = ''
                page += '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">\r\n'
                page += '<html>\r\n<head><title>%s %s</title></head>\r\n' % (code, line_info)
                page += '<body>\r\n<h1 style="color:#0066CC;">%s Unknown Status</h1><span style="color:#0066CC;">The requested URL %s encountered a %s.</span>\r\n' % (code, url, line_info)
                error = kwargs.get('error')
                if error:
                    page += '<div style="margin:20px;">%s</div>\r\n' % error
                page += '</body>\r\n</html>'
                self.content = page.encode(Constant.DECODE)

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

    # 封装并返回响应数据
    def setup_data(self):
        # 修改信息
        if not self.variable:
            self.variable = Variable()
        self.headers['Connection'] = self.variable.http_connection
        if not self.headers.get('Content-Length'):
            self.headers['Content-Length'] = len(self.content)
        # 封装
        self.data += (self.status_line + '\r\n').encode(Constant.DECODE)
        for key in self.headers.keys():
            val = self.headers[key]
            if key == 'Set-Cookie':
                for cookie in val:
                    self.data += ('%s: %s' % (key, cookie) + '\r\n').encode(Constant.DECODE)
            else:
                self.data += ('%s: %s' % (key, val) + '\r\n').encode(Constant.DECODE)
        self.data += '\r\n'.encode(Constant.DECODE)
        if self.variable.request_method != 'HEAD' and not self.status_code.startswith('30'):
            self.data += self.content
        error_flag = False
        # 除了500其他500系列错误不打印日志信息
        # 500 Series errors other than 500 do not print log information.
        if self.status_code == '500':
            error_flag = True

        return self.data, error_flag

    def set_response(self, response):
        self.status_code = response.status_code
        self.status_line = response.status_line
        self.headers = response.headers
        self.body = response.body
        self.content = response.content
        self.data = response.data
        self.session = response.session
