import requests
import lxml.html
import re


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
        'price': root.cssselect('.buy')[0].text(),
        'content': [h3.text_content() for h3 in root.cssselect('#content > h3')],
        }
    return ebook


def norm_spaces(res):
    return re.sub(r'\s+', ' ', res).strip()


def main():
    session = requests.Session()
    res = requests.get('https://gihyo.jp/dp')
    url_set = scrape_list_page(res)
    for u in url_set:
        res = session.get(u)
        ebook = scrape_detail_page(res)
        print(ebook)


if __name__ == '__main__':
    main()
