import threading
import socket

from service.socket_server.servers import httpserver


# 创建服务
class Server:

    # 线程锁
    lock = threading.Lock()
    # 连接的客户端列表
    clientList = []

    # 启动
    @classmethod
    def run(cls, lst, server_type):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(lst)
        s.listen(512)
        t = threading.Thread(target=cls.wait_connect, args=(s, server_type,))
        t.start()

    # 等待连接
    @classmethod
    def wait_connect(cls, s, server_type):
        while True:
            ss, address = s.accept()
            print('client %s is connection!' % (address[0]))
            cls.lock.acquire()
            cls.clientList.append((ss, address))
            cls.lock.release()
            cls.execute_work(ss, server_type)
            ss.close()

    # 执行任务
    @classmethod
    def execute_work(cls, ss, server_type):
        if server_type == 'http':
            httpserver(ss)
        elif server_type == 'proxy':
            print('研发中')
        elif server_type == 'socks':
            print('研发中')
