# 自定义方法类
from spango.service.developer import utils


def hello_world():
    json = utils.JsonObject()
    json.put('abc', '123')
    json.put('zxc', 456)
    return json.to_string()


def login(request, response, username, password):
    s = request.get('s')
    print(s)
    print("接收username:", username)
    print("接收password:", password)

    print(request.get_cookies())
    cookies = {
        'a': '123',
        'b': '456',
    }
    response.set_cookie(cookies)
    if username == 'abc' and password == '123':
        print('登录成功')
    else:
        print('用户名或密码错误：', username, password)
        print('提供账号：username=abc, password=123')
        response.redirect('/login')
    return response
