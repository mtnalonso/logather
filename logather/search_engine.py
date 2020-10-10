from abc import ABC, abstractmethod

import logather.tor_proxies


MIN_SOURCES = 30

BROWSER_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'q=0.8,en-US;q=0.5,en;q=0.3',
    'Acccept-Encoding': 'gzip, deflate',
    'Connection': 'close',
    'Upgrade-Insecure-Requests': '1',
}


class SearchEngine(ABC):
    def __init_subclass__(cls, **kwargs):
        cls._proxies = logather.tor_proxies.HTTP_PROXIES
        cls._headers = BROWSER_HEADERS
        super().__init_subclass__(**kwargs)

    @abstractmethod
    def _search(self):
        """Search log sources"""
        pass

    @abstractmethod
    def get_sources(self, min_sources=MIN_SOURCES):
        """Return found log locations"""
        pass
