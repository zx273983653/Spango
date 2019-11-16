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
