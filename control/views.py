# 自定义方法类


def hello_world():
    return 'HelloWorld'


def login(request, response, username, password):
    s = request.get('s')
    print(s)
    print("1111username:", username)
    print("2222password:", password)

    response.redirect('/')
    return response
