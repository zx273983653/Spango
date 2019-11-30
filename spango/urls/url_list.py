from control import urls


# url列表
class UrlList:
    urls = []

    @staticmethod
    def init():
        print('Load Urls.')
        # 添加urls
        add_url_lst = []
        rm_url_lst = []
        for url in urls.urls:
            if isinstance(url, list):
                add_url_lst = add_url_lst + url
                rm_url_lst.append(url)
        else:
            for rm_url in rm_url_lst:
                urls.urls.remove(rm_url)
        UrlList.urls = UrlList.urls + urls.urls + add_url_lst

    @staticmethod
    def set_up():
        UrlList.init()

    # 添加其他urls
    @staticmethod
    def set_urls(urls):
        UrlList.urls = UrlList.urls + urls

    # 匹配url
    @staticmethod
    def matching(path):
        for json in UrlList.urls:
            regex = json.get('regex')
            json['args'] = {}
            # 去掉连续重复的'/'和左右两边的'/',增加容错。
            while regex.find('//') != -1:
                regex.replace('//', '/')
            while path.find('//') != -1:
                path.replace('//', '/')
            if regex.startswith('/'):
                regex = regex[1:]
            elif regex.startswith('^/'):
                regex = '^' + regex[2:]
            if regex.endswith('/'):
                regex = regex[:-1]
            elif regex.endswith('/$'):
                regex = regex[:-2] + '$'
            if path.startswith('/'):
                path = path[1:]
            if path.endswith('/'):
                path = path[:-1]
            # 根据'/'切割path和正则
            path_blocks = path.split('/')
            regex_blocks = regex.split('/')
            if len(path_blocks) != len(regex_blocks):
                continue
            regex_block_index = 0
            for regex_block in regex_blocks:
                tmp_regex_block = regex_block
                if tmp_regex_block.startswith('^'):
                    tmp_regex_block = tmp_regex_block[1:]
                if tmp_regex_block.endswith('$'):
                    tmp_regex_block = tmp_regex_block[:-1]
                # 对字符串开头进行比对
                if regex_block_index == 0:
                    if regex_block.startswith('^'):
                        if regex_block.startswith('${') and (regex_block.endswith('}') or regex_block.endswith('}$')):
                            pass
                        elif not path_blocks[regex_block_index].startswith(tmp_regex_block):
                            break
                # 对字符串结尾进行比对
                if regex_block_index == len(regex_blocks) - 1:
                    if regex_block.endswith('$'):
                        if regex_block.startswith('${') and (regex_block.endswith('}') or regex_block.endswith('}$')):
                            pass
                        elif not path_blocks[regex_block_index].endswith(tmp_regex_block):
                            break
                # 对所有字符串进行比对
                if regex_block.startswith('${') and (regex_block.endswith('}') or regex_block.endswith('}$')):
                    if regex_block.endswith('}$'):
                        k = regex_block[2:-2]
                    else:
                        k = regex_block[2:-1]
                    v = path_blocks[regex_block_index]
                    json['args'][k] = v
                elif not path_blocks[regex_block_index].find(tmp_regex_block) != -1:
                    break

                # 匹配成功并返回结果
                if regex_block_index == len(regex_blocks) - 1:
                    return json
                regex_block_index += 1
