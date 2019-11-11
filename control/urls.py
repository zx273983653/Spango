from spango.urls import url
from control import views

'''
namespace:文件所在空间, 一般分为以下两种, 默认为 control。
如果是多级目录用.分开。如: namespace='templates.ss3'，此url的返回视图所在目录为templates/ss3。
处于static目录下的静态资源无需配置即可直接访问。
'''
CONTROL = 'control'
TEMPLATES = 'templates'

urls = [
    url('/index.html', view='index.html', namespace=TEMPLATES),
    url('/hello', view=views.hello_world)
]
