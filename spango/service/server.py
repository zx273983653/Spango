import threading
import socket

from spango.service.servers.http import httpserver
from spango.service.constant import Constant


# 创建服务
class Server:

    # 线程锁
    lock = threading.Lock()

    # 启动
    @staticmethod
    def run(lst, server_type, client_list):
        Server.server_type = server_type
        Server.client_list = client_list
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(lst)
        s.listen(Constant.concurrent_num)
        Server.sem = threading.Semaphore(Constant.concurrent_num)
        while True:
            ss, address = s.accept()
            ss.settimeout(Constant.time_out)
            if not Constant.ACCESS_LOG.upper() == 'FALSE':
                print('client %s is connection!' % (address[0]))
            t = threading.Thread(target=Server.wait_connect, args=(ss, address,))
            t.start()

    # 等待连接
    @staticmethod
    def wait_connect(ss, address):
        with Server.sem:
            # 加入连接列表
            Server.lock.acquire()
            Server.client_list.append((ss, address))
            Server.lock.release()
            # 执行业务
            Server.execute_work(ss)
            # 移除连接列表
            Server.lock.acquire()
            Server.client_list.remove((ss, address))
            Server.lock.release()
            # 关闭连接
            ss.close()

    # 执行任务
    @staticmethod
    def execute_work(ss):
        if Server.server_type == 'http':
            httpserver.HttpServer(ss)
        elif Server.server_type == 'task2':
            print("You chose a task that didn't start.")
        elif Server.server_type == 'task3':
            print("You chose a task that didn't start.")
