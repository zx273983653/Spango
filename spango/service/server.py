import threading
import socket

from spango.service.servers import httpserver


# 创建服务
class Server:

    # 线程锁
    lock = threading.Lock()
    # 连接的客户端列表
    clientList = []

    # 启动
    @classmethod
    def run(cls, lst, server_type):
        cls.server_type = server_type
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(lst)
        s.listen(512)
        while True:
            ss, address = s.accept()
            print('client %s is connection!' % (address[0]))
            t = threading.Thread(target=cls.wait_connect, args=(ss, address,))
            t.start()

    # 等待连接
    @classmethod
    def wait_connect(cls, ss, address):
        # 加入连接列表
        cls.lock.acquire()
        cls.clientList.append((ss, address))
        cls.lock.release()
        # 执行业务
        cls.execute_work(ss)
        # 关闭连接
        ss.close()
        # 移除连接列表
        cls.lock.acquire()
        cls.clientList.remove((ss, address))
        cls.lock.release()

    # 执行任务
    @classmethod
    def execute_work(cls, ss):
        if cls.server_type == 'http':
            httpserver.HttpServer(ss)
        elif cls.server_type == 'proxy':
            print('研发中')
        elif cls.server_type == 'socks':
            print('研发中')
