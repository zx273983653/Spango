from spango.service.developer import timer


def do():
    print('hello!')


def run():
    interval = 2  # 每次执行时间间隔
    timer.timer(interval, do)
