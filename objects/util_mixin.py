from typing import List, Callable

from settings import IMAGE_FORMATS


class UtilMixin:
    @staticmethod
    def format_check(url: str) -> bool:
        return 'http' in url

    @staticmethod
    def extensions_check(url: str) -> bool:
        return any([ex in url for ex in IMAGE_FORMATS])

    @staticmethod
    def sort_list(arr: List, key: Callable, reverse: bool = False) -> List:
        return sorted(arr, key=key, reverse=reverse)
