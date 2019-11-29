import os
from spango.utils import Properties


# 常量类，用于获取配置文件信息
class Constant:
    DECODE = 'utf-8'
    ENCODE = 'utf-8'

    @staticmethod
    def set_up():
        print('Load configuration information.')
        # 读取配置信息
        file_path = '%s%s' % (os.getcwd(), '/config/spjango.properties')
        props = Properties.parse(file_path)

        # 获取是否打印连接日志
        Constant.ACCESS_LOG = props.get('access_log')
        if not Constant.ACCESS_LOG:
            Constant.ACCESS_LOG = 'true'

        # 获取解码方式
        Constant.DECODE = props.get('decode')
        if not Constant.DECODE:
            Constant.DECODE = 'utf-8'

        # 获取编码方式
        Constant.ENCODE = props.get('encode')
        if not Constant.ENCODE:
            Constant.ENCODE = 'utf-8'

        # 获取编码方式
        Constant.DEFAULT_NET_INTERFACE = props.get('default_net_interface')
        if not Constant.DEFAULT_NET_INTERFACE:
            Constant.DEFAULT_NET_INTERFACE = '0.0.0.0'

        # 获取编码方式
        Constant.DEFAULT_PORT = props.get('default_port')
        if not Constant.DEFAULT_PORT:
            Constant.DEFAULT_PORT = 80
        else:
            Constant.DEFAULT_PORT = int(Constant.DEFAULT_PORT)

        # 请求头长度限制
        Constant.maxHttpHeaderSize = props.get('maxHttpHeaderSize')
        if not Constant.maxHttpHeaderSize:
            Constant.maxHttpHeaderSize = 3872131
        else:
            Constant.maxHttpHeaderSize = int(Constant.maxHttpHeaderSize)

        # url长度限制
        Constant.maxUrlSize = props.get('maxUrlSize')
        if not Constant.maxUrlSize:
            Constant.maxUrlSize = 3872131
        else:
            Constant.maxUrlSize = int(Constant.maxUrlSize)

        # 超时时间
        Constant.time_out = props.get('time_out')
        if not Constant.time_out:
            Constant.time_out = 8
        else:
            Constant.time_out = int(Constant.time_out)

        # 错误日志
        Constant.error_log = props.get('error_log')
        if not Constant.error_log:
            Constant.error_log = 'true'

        # 设置sessionCookieName
        Constant.sessionCookieName = props.get('sessionCookieName')

        # 设置session过期时间
        Constant.session_expires = props.get('session_expires')
        if not Constant.session_expires:
            Constant.session_expires = 30
        else:
            Constant.session_expires = int(Constant.session_expires)

        # 设置并发量
        Constant.concurrent_num = props.get('concurrent_num')
        if not Constant.concurrent_num:
            Constant.concurrent_num = 102
        else:
            Constant.concurrent_num = int(Constant.concurrent_num)

        # 配置目录情况
        Constant.ROOT_PATH = os.getcwd().replace('\\', '/')
        Constant.STATIC_PATH = Constant.ROOT_PATH + '/static/'
        Constant.TEMPLATES_PATH = Constant.ROOT_PATH + '/templates/'
