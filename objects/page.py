import operator
from collections import defaultdict
from typing import List, Union

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from objects.util_mixin import UtilMixin
from settings import PARSER


class Page(UtilMixin):
    status_code: int
    used_links = defaultdict(int)
    created_pages: list = []
    empty_links: List[str] = []
    sizes_sum: int = 0
    domain: str = ''

    def __init__(self, url: str, father=None, depth: int = 0) -> None:
        self.valid: bool = True
        self.url: str = url
        self.father: Page = father
        self.depth = depth + 1
        self.size: int
        self.soup: BeautifulSoup
        self.response: requests.Response = self.get_response()
        self.subpages: List[Page] = []
        self.out_links: List[str] = []
        self.used_urls: List[str] = []
        self.created_pages.append((url, self.depth))
        self.get_data()

    def __str__(self):
        return self.url

    def check_used_urls(self, url: str) -> bool:
        is_url_was_used = url in self.used_urls
        if self.father:
            return is_url_was_used or self.father.check_used_urls(url)
        return is_url_was_used

    def get_response(self) -> Union[requests.Response, None]:
        try:
            response = requests.get(self.url)
            self.status_code = response.status_code
            return response
        except ConnectionError:
            self.empty_links.append(self.url)
        self.valid = False
        return None

    def get_data(self) -> None:
        if self.valid:
            self.soup = self.get_soup()
            self.size = self.get_size()
            self.sizes_sum += self.size
            if not self.domain:
                self.domain = self.url
            self.find_url_links()

    def get_soup(self) -> BeautifulSoup:
        return BeautifulSoup(self.response.text, PARSER)

    def get_size(self) -> int:
        return len(self.soup.html)

    def categorise_links(self, url: str) -> None:
        if self.domain != url and not self.extensions_check(url):
            if self.domain in url:
                if not self.check_used_urls(url):
                    self.used_links[url] += 1
                    self.used_urls.append(url)
            elif self.format_check(url):
                if not self.check_used_urls(url):
                    self.used_links[url] += 1
                    self.out_links.append(url)

    def find_url_links(self) -> None:
        links = self.soup.select('a')
        for link in links:
            href = link.get('href')
            if href:
                self.categorise_links(href)
        for url in tqdm(self.used_urls, desc=self.url):
            if (url, self.depth + 1) not in self.created_pages:
                self.subpages.append(Page(url, self, self.depth))

    def get_longest_distance(self) -> List[tuple]:
        sort_pages = self.sort_list(self.created_pages, lambda x: x[1], True)
        return list(filter(lambda x: x[1] == sort_pages[0][1], sort_pages))

    def get_aver_number_of_empty(self) -> float:
        return len(self.empty_links)/len(self.used_links.keys())

    def get_aver_number_of_out_links(self) -> float:
        return len(self.out_links)/len(self.used_links.keys())

    def get_aver_number_of_internal_links(self) -> float:
        number_of_links = 0
        for val in self.used_links.values():
            number_of_links += val
        return number_of_links/len(self.used_links.keys())

    def get_aver_size_of_html(self) -> float:
        return self.sizes_sum/len(self.used_links.keys())

    def get_empty_links(self) -> List[str]:
        return self.empty_links

    def get_most_difficult_to_enter(self):
        return min(self.used_links.items(), key=operator.itemgetter(1))[0]

    def get_most_common_link(self) -> str:
        return max(self.used_links.items(), key=operator.itemgetter(1))[0]
