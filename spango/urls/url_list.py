from control import urls


# url列表
class UrlList:
    urls = []

    def __init__(self):
        # 添加默认urls
        self.urls = self.urls.extend(urls.urls)

    # 添加其他urls
    def set_urls(self, urls):
        self.urls = self.urls.extend(urls)

