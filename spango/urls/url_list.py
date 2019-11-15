from control import urls


# url列表
class UrlList:
    urls = []

    @staticmethod
    def init():
        print('Add default URLs.')
        # 添加默认urls
        UrlList.urls = UrlList.urls + urls.urls

    @staticmethod
    def set_up():
        UrlList.init()

    # 添加其他urls
    @staticmethod
    def set_urls(urls):
        UrlList.urls = UrlList.urls + urls

    # 匹配url
    @staticmethod
    def matching(url):
        for regex in UrlList.urls:
            if url.find(regex.get('regex')) != -1:
                return regex
