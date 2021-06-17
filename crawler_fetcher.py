import time

import requests
import lxml.html
import re
from pymongo import MongoClient


def scrape_list_page(res):
    root = lxml.html.fromstring(res.content)
    root.make_links_absolute(res.url)

    for a in root.cssselect('#listbook a[itemprop="url"]'):
        url = a.get('href')
        yield url


def scrape_detail_page(res):
    root = lxml.html.fromstring(res.content)
    ebook = {
        'url': res.url,
        'title': root.cssselect('#bookTitle')[0].text_context(),
        'price': root.cssselect('.buy')[0].text.strip(),
        'content': [norm_spaces(h3.text_content()) for h3 in root.cssselect('#content > h3')],
        }
    return ebook


def extract_key(url):
    m = re.search(r'/([^/]+)$', url)
    return m.group(1)


def norm_spaces(res):
    return re.sub(r'\s+', ' ', res).strip()


def main():
    client = MongoClient('localhost', 27017)
    collection = client.scraping.ebooks
    collection.create_index('key', unique=True)

    res = requests.get('https://gihyo.jp/dp')
    url_set = scrape_list_page(res)
    for u in url_set:
        key = extract_key(u)
        ebook = collection.find_one({'key': key})
        if not ebook:
            time.sleep(1)
            res = requests.get(u)
            ebook = scrape_detail_page(res)
            collection.insert_one(ebook)
        print(ebook)


if __name__ == '__main__':
    main()
