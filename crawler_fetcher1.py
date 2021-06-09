import requests
import lxml.html

def scrape_list_page(res):
    root = lxml.html.fromstring(res.content)
    root.make_links_absolute(res.url)

    for a in root.cssselect('#listbook a[itemprop="url"]'):
        url = a.get('href')
        yield(url)

res = requests.get('https://sample.scraping-book.com/dp/')
url_set = scrape_list_page(res)
for u in url_set:
    print(u)