from urllib import parse
import cgi
import os


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


# HTML解码
# HTML decode
def html_escape(s):
    return cgi.escape(s)


# 读取文件资源
# read file
def read_file(filename):
    if os.path.isfile(filename):
        # 获取文件名和扩展名
        name, extension_name = os.path.splitext(filename)
        # 封装文件内容
        content = bytes()
        with open(filename, "rb") as f:
            for line in f:
                content += line
            f.close()
        return content, name, extension_name
    else:
        return None, None, None
