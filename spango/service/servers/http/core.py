import os
from urllib import parse
from inspect import isfunction

from spango.service.constant import Constant
from spango.urls.url_list import UrlList


# 解析url
def parse_urls(url):
    proto = 80
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
    if path is None or path == '':
        path = '/'
    return proto, host, port, path


# 接收数据包
def receive_data(ss, request):
    while True:
        try:
            tmp_data = ss.recv(512)
        except ConnectionAbortedError:
            ss.close()
            return True

        request.content += tmp_data
        if request.content.find(b'\r\n\r\n') != -1:
            proto_data = request.content[:request.content.find(b'\r\n')]
            header_data = request.content[
                          request.content.find(b'\r\n') + 2:request.content.find(b'\r\n\r\n')]

            # 封装请求头
            header_lines = header_data.split(b'\r\n')
            for header_line in header_lines:
                tmp_key = header_line.split(b': ')[0]
                tmp_value = header_line.split(b': ')[1]
                request.headers[tmp_key.decode(Constant.DECODE)] = tmp_value.decode(Constant.DECODE)

            # 封装url
            request.url = proto_data[proto_data.find(b' ') + 1:proto_data.find(b' HTTP/')].decode(Constant.DECODE)

            # 封装查询字符串
            if request.url.find('?') != -1:
                request.search_str = request.url[request.url.find('?') + 1:]

            # 封装请求方式
            if proto_data.startswith(b'GET'):
                request.method = "GET"
                break
            elif proto_data.startswith(b'POST'):
                request.method = "POST"

                # 封装请求体
                len_body = int(request.headers.get('Content-Length'))
                if len_body:
                    request.body = request.content[request.content.find(b'\r\n\r\n') + 4:]
                    if len(request.body) >= len_body:
                        break
                else:
                    break

            elif proto_data.startswith(b'HEAD'):
                request.method = "HEAD"
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
    data = response.setup_data()
    ss.send(data)


# 接收与响应数据
def loop_data(ss, request, response, variable):
    n_do_while = True
    while n_do_while or variable.http_connection == 'keep-alive':
        n_do_while = False
        if receive_data(ss, request):
            break
        processing_data(request, response, variable)
        send_data(ss, response)


# 处理数据
def processing_data(request, response, variable):
    # 获取目录信息
    rootPath = Constant.ROOT_PATH
    static_path = Constant.STATIC_PATH
    templates_path = Constant.TEMPLATES_PATH

    if request.headers.get('Connection'):
        variable.http_connection = request.headers.get('Connection')
    response.variable = variable

    print("收到请求头：", request.headers)
    try:
        if request.body:
            print("收到请求体：", request.body.decode(Constant.DECODE))
    except UnicodeDecodeError:
        print("收到请求体：", request.body)
    print("收到FormData：", request.data_block)

    print("接收的url：", request.url)
    print("收到查询字符串：", request.search_str)
    print("接收单个参数abc", request.get('abc'))
    aaa = request.gets('abc')
    print("接收数组参数abc", aaa)

    # url长度限制校验
    if request.url is None or len(request.url) > Constant.maxUrlSize:
        response.set_status('400')
        return

    regex = UrlList.matching(request.url)
    print('匹配到：', regex)
    if regex is None:
        # 匹配静态资源
        if request.url.find('?') != -1:
            filename = static_path + request.url[:request.url.find('?')]
        else:
            filename = static_path + request.url
        content = read_file(filename)
        if content:
            response.content = content
        else:
            # 返回404
            response.set_status('404', url=request.url)

        return

    if isinstance(regex.get('view'), str):
        filename = templates_path + regex.get('view')
        content = read_file(filename)
        response.content = content
    elif isfunction(regex.get('view')):
        print(222222222222222222)
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
