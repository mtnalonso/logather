import requests

from logather.startpage import Startpage
from logather.tor_proxies import HTTP_PROXIES
from logather.validator import Validator


class Logather:
    def __init__(self, min_potential_sources=50):
        self.min_potential_sources = min_potential_sources
        self.validation_timeout = 10.0
        self.ip_check_url = 'http://httpbin.org/ip'
        pass

    def gather(self):
        print('Using ip: {}'.format(self._get_proxy_ip()))

        sp = Startpage()
        sources = sp.get_sources(self.min_potential_sources)
        
        validator = Validator(validation_timeout=self.validation_timeout)
        valid_sources = validator.validate(sources)

        return valid_sources

    def _get_proxy_ip(self):
        response = requests.get(self.ip_check_url, proxies=HTTP_PROXIES)
        return response.text
