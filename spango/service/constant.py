import os
from spango.utils import Properties


# 常量类，用于获取配置文件信息
class Constant:
    DECODE = 'utf-8'
    ENCODE = 'utf-8'

    # 读取配置信息
    file_path = '%s%s' % (os.getcwd(), '/config/spjango.properties')
    props = Properties.parse(file_path)

    # 获取解码方式
    DECODE = props.get('decode')
    if not DECODE:
        DECODE = 'utf-8'

    # 获取编码方式
    ENCODE = props.get('encode')
    if not ENCODE:
        ENCODE = 'utf-8'

    # 获取编码方式
    DEFAULT_NET_INTERFACE = props.get('default_net_interface')
    if not DEFAULT_NET_INTERFACE:
        DEFAULT_NET_INTERFACE = '0.0.0.0'

    # 获取编码方式
    DEFAULT_PORT = props.get('default_port')
    if not DEFAULT_PORT:
        DEFAULT_PORT = 80
    else:
        DEFAULT_PORT = int(DEFAULT_PORT)
