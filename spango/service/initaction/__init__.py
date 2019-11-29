from spango.service.constant import Constant
from spango.urls.url_list import UrlList
from spango.service.servers.http.session import Session


# 初始化配置信息
def action():
    print('Perform some initialization information:')
    Constant.set_up()
    UrlList.set_up()
    Session.set_up()
