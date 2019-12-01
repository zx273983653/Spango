import threading
import time


def timer(interval, func, later=False):
    '''
    timer
    :param interval:  时间间隔
    :param func:  执行函数
    :param later:  是否先等待，默认False
    '''
    t = threading.Thread(target=__run, args=(interval, func, later))
    t.setDaemon(True)
    t.start()


def __run(interval, func, later):
    if later:
        time.sleep(interval)
    while True:
        func()
        time.sleep(interval)
