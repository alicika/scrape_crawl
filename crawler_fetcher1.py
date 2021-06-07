import requests
import lxml.html

res = requests.get('https://sample.scraping-book.com/dp/')
root = lxml.html.fromstring(res.content)
for a in root.cssselect('a[itemprop="url"]'):
    url = a.get('href')
    print(url)