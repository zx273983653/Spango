import argparse
import threading
import time
from spango.service import server
from spango.service.constant import Constant
from spango.service import initaction


# 获取参数
def get_parser_params():
    # 初始化配置信息
    initaction.action()

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

    # 正在连接的客户端列表
    client_list = []

    # 启动服务
    t = threading.Thread(target=server.Server.run, args=(lst, server_type, client_list))
    t.setDaemon(True)
    t.start()

    try:
        while True:
            # 使用Ctrl + c 终止服务
            # time.sleep(60)

            # 输入ls查看当前连接，输入任意键其他键终止服务
            cmd = input()
            if cmd == 'ls':
                print('当前连接：')
                for client in client_list:
                    print(client[1])

    except KeyboardInterrupt:
        print('---------------------------------------------')
        print('END')
