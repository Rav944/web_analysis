import sys
from pprint import pprint

import argh

from objects.page import Page

sys.setrecursionlimit(10000)


@argh.arg('url', help='Address to scrap')
def scraper(url: str):
    page = Page(url)
    print('Longest Distances: ')
    pprint(page.get_longest_distance())
    print(f'AVG number of empty links: {page.get_aver_number_of_empty()}')
    print(f'AVG number of out links: {page.get_aver_number_of_out_links()}')
    print(f'AVG number of internal links: {page.get_aver_number_of_internal_links()}')
    print(f'AVG HTML size: {page.get_aver_size_of_html()}')
    print('Empty links: ')
    pprint(page.get_empty_links())
    print('Most difficult to enter: ')
    pprint(page.get_most_difficult_to_enter())
    print('Most linked:')
    pprint(page.get_most_common_link())


if __name__ == '__main__':
    argh.dispatch_commands([scraper])
