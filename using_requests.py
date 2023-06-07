import os
from concurrent.futures import ThreadPoolExecutor
from itertools import chain
from multiprocessing import Pool
from time import time
from typing import List
from urllib.parse import urlparse

import requests as requests
from bs4 import BeautifulSoup

url = 'https://www.google.com/search?q=howard'
headers = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
    )
}
LINKS_TO_GET = 50
TEXTS_TO_GET = 50


def call_measuring_time(func):
    def wrapper(*args, **kwargs):
        start = time()
        print(f'Starting {func.__name__}')
        func(*args, **kwargs)
        end = time()
        print(f'{func.__name__} took {end - start} seconds')

    return wrapper


def get_texts_from_link(link) -> List[str]:
    response = requests.get(link, headers=headers, timeout=2)
    return get_texts(response.text)


def report_texts(title, texts):
    print(f'{title} texts: {", ".join(sorted(texts))}')


def get_links_to_scrap():
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    all_links = [x.find('a')['href'] for x in soup.find_all('div', class_='g')]
    valid_links = [x for x in all_links if urlparse(x).scheme][:LINKS_TO_GET]
    return valid_links


def get_texts(page):
    bs = BeautifulSoup(page, 'html.parser')
    all_texts = [x.text.replace('\n', '')
                 for x in bs.find_all('span')
                 if x.text]
    valid_texts = [x.strip() for x in all_texts if len(x.strip()) > 4]
    return valid_texts[:TEXTS_TO_GET]


@call_measuring_time
def singlethread():
    valid_links = get_links_to_scrap()
    texts = [get_texts_from_link(link) for link in valid_links]
    flattened_texts = list(chain.from_iterable(texts))
    report_texts('Singlethread', flattened_texts)


@call_measuring_time
def multithread():
    valid_links = get_links_to_scrap()
    num_workers = min(LINKS_TO_GET, os.cpu_count())
    print(f'Using {num_workers} workers')
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        texts = executor.map(get_texts_from_link, valid_links)
    flattened_texts = list(chain.from_iterable(texts))
    report_texts('Multithread', flattened_texts)


@call_measuring_time
def multiproc():
    valid_links = get_links_to_scrap()
    num_procs = min(LINKS_TO_GET, os.cpu_count())
    print(f'Using {num_procs} processes')
    with Pool(num_procs) as executor:
        texts = executor.map(get_texts_from_link, valid_links)
    flattened_texts = list(chain.from_iterable(texts))
    report_texts('Multiprocess', flattened_texts)


def main():
    singlethread()
    multithread()
    multiproc()


if __name__ == '__main__':
    main()
