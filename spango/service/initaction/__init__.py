from spango.service.constant import Constant
from spango.urls.url_list import UrlList
from spango.service.servers.http.session import Session
from spango.service.servers import server_timer


# 初始化配置信息
def action():
    print('Perform some initialization information:')
    Constant.set_up()
    UrlList.set_up()
    Session.set_up()
    server_timer.timer4server(30)
    if Constant.server_timer:
        from service.server import timer
        timer.run()
