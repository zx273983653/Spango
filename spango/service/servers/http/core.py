import socket
from inspect import isfunction
import os
from spango.utils import filetype
from spango.error import SpError
from spango.service.constant import Constant
from spango.urls.url_list import UrlList
from spango.utils import parse_urls
from spango.utils import html_escape
from spango.service.developer.http import Request
from spango.service.developer.http import Response
from spango.service.servers.http.session import Session


# 接收数据包
# receive packets
def receive_data(ss, request, response):
    while True:
        try:
            tmp_data = ss.recv(512)
            if tmp_data == b'':
                return True
        except socket.timeout:
            return True
        except ConnectionAbortedError:
            return True
        except OSError:
            return True
        except Exception as e:
            raise e

        request.content += tmp_data
        if request.content.find(b'\r\n\r\n') != -1:
            request.status_line = request.content[:request.content.find(b'\r\n')]
            header_data = request.content[
                          request.content.find(b'\r\n') + 2:request.content.find(b'\r\n\r\n')]

            # 封装请求头
            # pack request headers
            header_lines = header_data.split(b'\r\n')
            for header_line in header_lines:
                if header_line.find(b': ') == -1:
                    continue
                tmp_key = header_line.split(b': ')[0]
                tmp_value = header_line.split(b': ')[1]
                if tmp_key.decode(Constant.DECODE).upper() == 'COOKIE':
                    cookie_dict = {}
                    tmp_cookie_lst1 = tmp_value.decode(Constant.DECODE).split('; ')
                    for cookie1 in tmp_cookie_lst1:
                        tmp_cookie_lst2 = cookie1.split('=')
                        if len(tmp_cookie_lst2) == 2:
                            cookie_dict[tmp_cookie_lst2[0]] = tmp_cookie_lst2[1]
                    request.headers['Cookie'] = cookie_dict
                else:
                    request.headers[tmp_key.decode(Constant.DECODE)] = tmp_value.decode(Constant.DECODE)

            # 封装url
            # pack url
            request.url = request.status_line[request.status_line.find(b' ') + 1:request.status_line.find(b' HTTP/')].decode(Constant.DECODE)

            # 封装查询字符串
            # pack query string
            if request.url.find('?') != -1:
                request.search_str = request.url[request.url.find('?') + 1:]

            # 封装请求方式
            # pack request method
            status_line_arr = request.status_line.split(b' ')
            if len(status_line_arr) != 3:
                response.set_status('400', url=request.url)
                return 0
            else:
                if status_line_arr[0] == b'GET':
                    request.method = "GET"
                    break
                elif status_line_arr[0] == b'POST':
                    request.method = "POST"

                    # 封装请求体
                    # pack request body
                    len_body = int(request.headers.get('Content-Length'))
                    if len_body:
                        request.body = request.content[request.content.find(b'\r\n\r\n') + 4:]
                        if len(request.body) >= len_body:
                            break
                    else:
                        break

                elif status_line_arr[0] == b'HEAD':
                    request.method = "HEAD"
                    break
                else:
                    print('__error__:目前不支持该请求方式')
                    print('__error__:Request method is not supported temporarily.')
                    response.set_status('501', url=request.url, error='Request method is not supported temporarily.', line_info='Not Implemented')
                    return 0

    # 处理form-data发包方式
    # handle form-data
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
# send data
def send_data(ss, response, filename=None):
    if filename:
        # 获取文件名和扩展名
        name, extension_name = os.path.splitext(filename)
        content_type = filetype.content_type_list.get(extension_name)
        # 封装文件内容
        with open(filename, "rb") as f:
            first_flag = True
            while True:
                data = f.read(4096)
                if first_flag:
                    first_flag = False
                    file_size = os.path.getsize(filename)
                    response.headers['Content-Length'] = file_size
                    if content_type:
                        response.headers['Content-Type'] = content_type
                    if data:
                        response.content = data
                    data, error_flag = response.setup_data()
                    if error_flag and Constant.error_log.upper() == 'TRUE':
                        raise SpError(response.error)

                try:
                    ss.send(data)
                except ConnectionAbortedError:
                    pass
                if data == b"":
                    break
        f.close()
    else:
        data, error_flag = response.setup_data()
        if error_flag and Constant.error_log.upper() == 'TRUE':
            raise SpError(response.error)
        try:
            ss.send(data)
        except ConnectionAbortedError:
            pass


# 处理数据
# handle data
def processing_data(request, response, variable):
    # 获取目录信息
    # get catalog information
    rootPath = Constant.ROOT_PATH
    static_path = Constant.STATIC_PATH
    templates_path = Constant.TEMPLATES_PATH

    # 封装变量
    # pack variables
    variable.request_method = request.method
    if request.headers.get('Connection'):
        if request.headers.get('Connection').lower() == 'keep-alive':
            variable.http_connection = 'Keep-Alive'
        # 由于默认是'close' 所以注释掉下面两行
        # Because the default is 'close'.comment out the following two lines.
        # elif request.headers.get('Connection').lower() == 'close':
        #     variable.http_connection = 'close'
    response.variable = variable

    # 设置session
    if Constant.sessionCookieName:
        cookie_dict = request.headers.get('Cookie')
        if cookie_dict:
            cre_s_flag = True
            for cookie_key in cookie_dict.keys():
                if cookie_key == Constant.sessionCookieName:
                    session_ = Session.init_expires(cookie_dict.get(cookie_key))
                    if session_:
                        cre_s_flag = False
                        request.session = session_
                        break
                    else:
                        break

            if cre_s_flag:
                session_, session_id = Session.create_session()
                request.session = session_
                response.session = session_
                response.set_cookie({Constant.sessionCookieName: session_['id']})

    # url长度限制校验
    # url length restriction
    if request.url is None or len(request.url) > Constant.maxUrlSize:
        response.set_status('400', url=request.url)
        return

    # 请求长度校验
    # request length restriction
    if Constant.maxHttpContentSize:
        if len(request.content) > Constant.maxHttpContentSize:
            response.set_status('403', url=request.url, line_info='Access Denied', error='Reason: Reqeust length is too long.')
            return

    # 解析url
    # parse url
    proto, host, port, path, query = parse_urls(request.url)
    path = path.strip()

    # 设置默认访问路径
    # set default access path
    if path == '/':
        path = '/index.html'

    regex_json = UrlList.matching(path)
    if not Constant.ACCESS_LOG.upper() == 'FALSE':
        if regex_json:
            print('Request interface:', regex_json)
    if regex_json is None:
        # 匹配静态资源
        filename = static_path + path
        if not os.path.isfile(filename):
            response.set_status('404', url=request.url)
            return

        return filename

    if isinstance(regex_json.get('view'), str):
        filename = templates_path + regex_json.get('view')
        if not os.path.isfile(filename):
            response.set_status('500', url=request.url, error='系统找不到文件：' + filename)
            return
        else:
            return filename

    elif isfunction(regex_json.get('view')):
        func = regex_json.get('view')
        args = regex_json.get('args')
        # 获取函数参数列表
        # get function list
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
        return


# 接收与响应数据
# reception and response data
def loop_data(ss, request, response, variable):
    n_do_while = True
    while n_do_while or variable.http_connection.lower() == 'keep-alive':
        n_do_while = False
        # 初始化变量
        # initialize variable
        request.set_initialize()
        response.set_initialize()
        variable.set_initialize()

        receive_status = receive_data(ss, request, response)
        if receive_status:
            break
        elif receive_status == 0:
            # Direct discarding
            send_data(ss, response)
            break
        filename = processing_data(request, response, variable)
        send_data(ss, response, filename=filename)
