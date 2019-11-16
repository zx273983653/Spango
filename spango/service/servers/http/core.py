from urllib import parse
from spango.service.constant import Constant


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
        tmp_data = ss.recv(1024)
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
                len_body = request.headers.get('Content-Length')
                if len_body:
                    request.body = request.content[request.content.find(b'\r\n\r\n') + 4:]
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
