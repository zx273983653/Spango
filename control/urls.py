from spango.urls import url
from control import views

'''
使用示例：
1. /index.html 返回跟目录下 index.html。(优先检索templates目录，然后检索static目录)
2. /hello 跳进views.hello_world方法中进行处理。
3. /login/${username}/${password} 路径类型的入参方式，其中username，password为参数，可在views.login中接收参数。
'''

urls = [
    url('/index.html', view='index.html'),
    url('/hello', view=views.hello_world),
    url('/login/${username}/${password}', view=views.login)
]
