import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = curPath[:curPath.find('spango')]
static_path = rootPath + 'static'
templates_path = rootPath + 'templates'


# 读取文件资源
def read_file(filename):
    content = bytes()
    with open(filename, "rb") as f:
        for line in f:
            content += line
        f.close()
    return content


if __name__ == '__main__':
    filename = templates_path + '/index.html'
    print(filename)
    content = read_file(filename)
    print(content)
