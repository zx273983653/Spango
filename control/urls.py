from spango.urls import *
from control import views

from control import urls2
'''
使用示例：
/index.html 如view=str则直接返回静态资源。(优先检索templates目录，然后检索static目录)
hello 跳进views.hello_world方法中进行处理。
/login/${username}/${password} 路径类型的入参方式，其中username，password为参数，可在views.login中接收参数。
模糊匹配：'/index' 可以匹配任意带有“/index”的路径，如 /index123、/abc/index123。
精准匹配：“^”匹配字符串的开头，“$”匹配字符串尾。强制限制url以什么开头，以什么结尾。
include 合并其他文件的urls
'''

urls = [
    url('^/index.html$', view='index.html'),
    url('^/index', view='index123.html'),
    url('hello', view=views.hello_world),
    url('^login$', view='login/login.html'),
    url('^login/${username}/${password}', view=views.login),

    # 添加其他文件的urls
    include(urls2.urls),
]
