import requests

url = 'http://47.244.17.247'
res = requests.get(url)
headers = res.headers
print(headers)
content = res.content
print(content)
print(111111, len(content))
