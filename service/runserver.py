import argparse

from service.socket_server import server


# 获取参数
def get_parser_params():
    # 命令行参数解析对象
    parser = argparse.ArgumentParser()
    parser.add_argument('-ip', dest='listen_ip', default='0.0.0.0', help='Listen Host(default=0.0.0.0)')
    parser.add_argument('-port', dest='listen_port', type=int, default=80, help='Listen Port(default=80)')
    parser.add_argument('-server', dest='server', default='http', help='Server Type default=http')
    # 解析命令行参数
    args = parser.parse_args()
    listen_ip = args.listen_ip
    listen_port = args.listen_port
    server_type = args.server

    if listen_ip is None or listen_port is None or server is None:
        print(parser.parse_args(['-h']))
        exit(0)
    else:
        return listen_ip, listen_port, server_type


if __name__ == '__main__':
    listen_ip, listen_port, server_type = get_parser_params()
    print("Listening: %s:%d" % (listen_ip, listen_port))
    lst = (listen_ip, listen_port)
    print(lst[1])

    server.Server.run(lst, server_type)
