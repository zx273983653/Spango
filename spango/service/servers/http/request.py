from multidict import CIMultiDict
from urllib import parse
from spango.service.constant import Constant


class HttpRequest:
    # 请求的原始数据
    content = bytes()
    # 状态行
    status_line = None
    # 请求头
    headers = CIMultiDict()
    # 请求方式
    method = None
    # 请求URL
    url = None
    # 查询字符串
    search_str = None
    # 请求体
    body = None
    # form-data方式时一些参数
    data_block = []

    # 获取参数
    def get(self, param):
        if self.method == 'POST' and self.body and (self.headers.get('Content-Type') is None or self.headers.get('Content-Type').find('multipart/form-data') == -1):
            if self.search_str:
                self.search_str += "%s%s" % ('&', self.body)
            else:
                self.search_str = "%s%s" % ('&', self.body)

        if self.search_str:
            args_blocks = self.search_str.split('&')
            for args in args_blocks:
                if args.find('=') != -1:
                    tmp_key = args[:args.find('=')]
                    tmp_val = args[args.find('=') + 1:]
                    if param == tmp_key:
                        # url解码并返回
                        return parse.unquote(tmp_val)

        # 处理form-data发包方式
        if self.headers.get('Content-Type') and self.headers.get('Content-Type').find(
                'multipart/form-data') != -1:
            if self.body:
                for once_block in self.data_block:
                    data_name = once_block.get('data_name')
                    if data_name and param == data_name.decode(Constant.DECODE):
                        return once_block.get('data_value')

        return None

    # 获取集合类型参数
    def gets(self, params):
        if self.method == 'POST' and self.body and (self.headers.get('Content-Type') is None or self.headers.get('Content-Type').find('multipart/form-data') == -1):
            if self.search_str:
                self.search_str += "%s%s" % ('&', self.body)
            else:
                self.search_str = "%s%s" % ('&', self.body)

        r_list = []
        if self.search_str:
            args_blocks = self.search_str.split('&')
            if len(args_blocks) > 0:
                for args in args_blocks:
                    if args.find('=') != -1:
                        tmp_key = args[:args.find('=')]
                        tmp_val = args[args.find('=') + 1:]
                        if params == tmp_key:
                            # url解码并添加至列表
                            r_list.append(parse.unquote(tmp_val))

        # 处理form-data发包方式
        if self.headers.get('Content-Type') and self.headers.get('Content-Type').find('multipart/form-data') != -1:
            if self.body:
                for once_block in self.data_block:
                    data_name = once_block.get('data_name')
                    if data_name and params == data_name:
                        r_list.append(once_block.get('data_value'))

        if len(r_list) > 0:
            return r_list
        else:
            return None
