import argparse
import threading
import time
from spango.service import server
from spango.service.constant import Constant


# 获取参数
def get_parser_params():
    # 命令行参数解析对象
    parser = argparse.ArgumentParser()
    parser.add_argument('-ip', dest='listen_ip', default=Constant.DEFAULT_NET_INTERFACE, help='Listen Host(default=%s)' % Constant.DEFAULT_NET_INTERFACE)
    parser.add_argument('-port', dest='listen_port', type=int, default=Constant.DEFAULT_PORT, help='Listen Port(default=%d)' % Constant.DEFAULT_PORT)
    parser.add_argument('-server', dest='server', default='http', help='Server Type default=http')
    # 解析命令行参数
    args = parser.parse_args()
    listen_ip = args.listen_ip
    listen_port = args.listen_port
    server_type = args.server

    if listen_ip is None or listen_port is None or server_type is None:
        print(parser.parse_args(['-h']))
        exit(0)
    else:
        if listen_ip == '0':
            listen_ip = '0.0.0.0'
        return listen_ip, listen_port, server_type


def run():
    # 获取启动参数
    listen_ip, listen_port, server_type = get_parser_params()
    print("Listening: %s:%d" % (listen_ip, listen_port))
    lst = (listen_ip, listen_port)

    # 子线程启动服务
    t = threading.Thread(target=server.Server.run, args=(lst, server_type,))
    t.setDaemon(True)
    t.start()

    # 使用Ctrl + c 终止服务
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print('---------------------------------------------')
        print('END')
