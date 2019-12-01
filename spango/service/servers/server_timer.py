import threading
import time
from spango.service.servers.http.session import Session


def run(interval):
    while True:
        time.sleep(interval)
        # 更新一下session列表
        Session.rm_expires()


# 服务端定时器
def timer4server(interval):
    t = threading.Thread(target=run, args=(interval,))
    t.setDaemon(True)
    t.start()
