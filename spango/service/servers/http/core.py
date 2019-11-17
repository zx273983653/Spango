import os
import socket
from urllib import parse
import cgi
from inspect import isfunction

from spango.error import SpError
from spango.service.constant import Constant
from spango.urls.url_list import UrlList
from spango.service.developer.http import Request
from spango.service.developer.http import Response


# 解析url
def parse_urls(url):
    proto = 'http'
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
    query = up.query
    if path is None or path == '':
        path = '/'
    return proto, host, port, path, query


# 接收数据包
def receive_data(ss, request):
    while True:
        try:
            tmp_data = ss.recv(512)
        except socket.timeout:
            return True
        except ConnectionAbortedError:
            return True
        except OSError:
            return True
        except Exception as e:
            raise e
            return True

        request.content += tmp_data
        if request.content.find(b'\r\n\r\n') != -1:
            request.status_line = request.content[:request.content.find(b'\r\n')]
            header_data = request.content[
                          request.content.find(b'\r\n') + 2:request.content.find(b'\r\n\r\n')]

            # 封装请求头
            header_lines = header_data.split(b'\r\n')
            for header_line in header_lines:
                tmp_key = header_line.split(b': ')[0]
                tmp_value = header_line.split(b': ')[1]
                request.headers[tmp_key.decode(Constant.DECODE)] = tmp_value.decode(Constant.DECODE)

            # 封装url
            request.url = request.status_line[request.status_line.find(b' ') + 1:request.status_line.find(b' HTTP/')].decode(Constant.DECODE)

            # 封装查询字符串
            if request.url.find('?') != -1:
                request.search_str = request.url[request.url.find('?') + 1:]

            # 封装请求方式
            if request.status_line.startswith(b'GET'):
                request.method = "GET"
                break
            elif request.status_line.startswith(b'POST'):
                request.method = "POST"

                # 封装请求体
                len_body = int(request.headers.get('Content-Length'))
                if len_body:
                    request.body = request.content[request.content.find(b'\r\n\r\n') + 4:]
                    if len(request.body) >= len_body:
                        break
                else:
                    break

            elif request.status_line.startswith(b'HEAD'):
                request.method = "HEAD"
                break
            else:
                print('__error__:目前不支持该请求方式')
                break

    # 处理form-data发包方式
    if request.headers.get('Content-Type') and request.headers.get('Content-Type').find(
            'multipart/form-data') != -1:
        if request.body:
            boundary = request.body[:request.body.find(b'\r\n')]
            data_blocks = request.body.split(boundary)
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
                    request.data_block.append(data_block_dict)


# 发送数据
def send_data(ss, response):
    data, error_flag = response.setup_data()
    try:
        ss.send(data)
    except ConnectionAbortedError:
        pass
    if error_flag and Constant.error_log.upper() != 'FALSE':
        raise SpError(response.error)


# 接收与响应数据
def loop_data(ss, request, response, variable):
    n_do_while = True
    while n_do_while or variable.http_connection == 'keep-alive':
        n_do_while = False
        if receive_data(ss, request):
            variable.http_connection == 'close'
            break
        processing_data(request, response, variable)
        send_data(ss, response)


# 处理数据
def processing_data(request, response, variable):
    # 获取目录信息
    rootPath = Constant.ROOT_PATH
    static_path = Constant.STATIC_PATH
    templates_path = Constant.TEMPLATES_PATH

    # 封装变量
    variable.request_method = request.method
    if request.headers.get('Connection'):
        variable.http_connection = request.headers.get('Connection')
    response.variable = variable

    # url长度限制校验
    if request.url is None or len(request.url) > Constant.maxUrlSize:
        response.set_status('400', url=request.url)
        return

    # 解析url
    proto, host, port, path, query = parse_urls(request.url)
    path = path.strip()

    # 设置默认访问路径
    if path == '/':
        path = '/index.html'

    regex_json = UrlList.matching(path)
    if not Constant.ACCESS_LOG.upper() == 'FALSE':
        print('Request interface:', regex_json)
    if regex_json is None:
        # 匹配静态资源
        filename = static_path + path
        content = read_file(filename)
        if content:
            response.content = content
        else:
            response.set_status('404', url=request.url)
        return

    if isinstance(regex_json.get('view'), str):
        filename = templates_path + regex_json.get('view')
        content = read_file(filename)
        if content:
            response.content = content
        else:
            response.set_status('500', url=request.url, error='系统找不到文件：' + filename)
            return
    elif isfunction(regex_json.get('view')):
        func = regex_json.get('view')
        args = regex_json.get('args')
        # 获取函数参数列表
        f_args = func.__code__.co_varnames

        parameter = {}
        for arg in f_args:
            if 'request' == arg:
                parameter['request'] = Request(request)
            elif 'response' == arg:
                parameter['response'] = Response(response)
            else:
                for k in args.keys():
                    if arg == k:
                        parameter[k] = args[k]
        if func.__code__.co_argcount != len(parameter):
            error = '接口参数列表长度不正确。应该为：%d，实际为：%d' % (len(parameter), func.__code__.co_argcount)
            response.set_status('500', url=request.url, error=error)
            return

        tmp_response = func(**parameter)
        if isinstance(tmp_response, str):
            response.content = tmp_response.encode(Constant.DECODE)
        elif isinstance(tmp_response, Response):
            response.set_response(tmp_response)
        else:
            response.set_status('500', url=request.url, error='未知的返回值类型：' + html_escape(str(type(tmp_response))))
            return

    else:
        print('无法处理的url')


# 读取文件资源
def read_file(filename):
    if os.path.isfile(filename):
        content = bytes()
        with open(filename, "rb") as f:
            for line in f:
                content += line
            f.close()
        return content


# HTML解码
def html_escape(s):
    return cgi.escape(s)
