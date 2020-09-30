import requests
import json
from bs4 import BeautifulSoup

from logather.tor_proxies import HTTP_PROXIES


MIN_SOURCES = 30


browser_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'q=0.8,en-US;q=0.5,en;q=0.3',
    'Acccept-Encoding': 'gzip, deflate',
    'Connection': 'close',
    'Origin': 'https://startpage.com',
    'Upgrade-Insecure-Requests': '1',
}


class Startpage:
    def __init__(self, proxies=HTTP_PROXIES):
        self._headers = browser_headers
        self._proxies = proxies
        self._base_url = 'https://startpage.com/'
        self._search_url = 'https://startpage.com/sp/search'
        self._log_query = 'inurl:(access.log | error.log) filetype:log "GET /"'

    def _search(self, sc=None, page_number=None):
        sc = sc or self._get_initial_sc_value()
        data = self._build_post_data(sc, page_number) 

        response = requests.post(
            self._search_url,
            proxies=self._proxies,
            headers=self._headers,
            data=data
        )
        
        soup = BeautifulSoup(response.content, 'html.parser')
        results = soup.findAll('a', {'class': 'w-gl__result-title'})
        sc = soup.findAll('input', {'name': 'sc'})[0].get('value')

        links = [result['href'] for result in results]
        print('[+] Got {} potential log sources'.format(len(links)))
        return links, sc

    def _build_post_data(self, sc, page_number=None):
        post_data = {
            'query': self._log_query,
            'language': 'english',
            'lui': 'english',
            'cat': 'web',
            'sc': sc,
            'abp': '-1',
        }
        if page_number:
            post_data['page'] = page_number
        return post_data

    def _get_initial_sc_value(self):
        print('[*] Getting initial sc value')
        response = requests.get(
            self._base_url, proxies=self._proxies, headers=self._headers
        )
        html = response.content.decode('utf-8')
        self.sc = html.split('name="sc" value="')[1].split('"')[0]
        return self.sc

    def get_sources(self, min_number=MIN_SOURCES):
        sources = []
        current_results_page = 1
        sc = self._get_initial_sc_value()

        while len(sources) < min_number:
            links, sc = self._search(sc, current_results_page)
            sources.extend(links)
            current_results_page += 1
        return sources

