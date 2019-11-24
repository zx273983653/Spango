import requests
from bs4 import BeautifulSoup

url = 'https://tool.oschina.net/commons'
res = requests.get(url)
html_doc = res.text

# print(html_doc)
soup = BeautifulSoup(html_doc)
tbody = soup.find('table', class_='toolTable table').find('tbody')
td1s = tbody.findAll('td')

s1 = None
s2 = None
n = 0
for td in td1s:
    n += 1
    if n % 2 == 0:
        s2 = td.text
        print("'%s': '%s'," % (s1, s2))
        s1 = None
        s2 = None
    else:
        s1 = td.text

