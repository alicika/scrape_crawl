import requests
import queue
from bs4 import BeautifulSoup
from threading import Thread

visited = set()
to_visit = set()
max_visits = 3
URL = "https://scrapeme.live/shop/page/1/"
data = []
num_workers = 5


def queue_worker(_, q):
    while True:
        url = q.get()
        print("processing...", url)
        if len(visited) < max_visits and url not in visited:
            visited.add(url)
            print("Crawl: ", url)
            html = get_html(url)
            soup = BeautifulSoup(html, "html.parser")
            extract_content(soup)
            links = extract_links(soup)
            for link in links:
                if link not in visited:
                    q.put(link)
        q.task_done()


def get_html(url):
    try:
        return requests.get(url).content
    except Exception as e:
        print(e)
        return ""


def extract_links(soup):
    return [a.get('href') for a in soup.select('a.page-numbers') if a.get('href') not in visited]


def extract_content(soup):
    for product in soup.select('.product'):
        data.append({
            'id': product.find('a', attrs={'data-product_id': True})['data-product_id'],
            'name': product.find('h2').text,
            'price': product.find(class_='amount').text
        })


def main():
    q = queue.Queue()
    for i in range(num_workers):
        Thread(target=queue_worker, args=(i, q), daemon=True).start()
    q.put(URL)
    q.join()
    print("Done!")
    print(visited)
    print(data)


if __name__ == '__main__':
    main()
