import re
from threading import Thread
from queue import Queue

import requests

from tor_proxies import HTTP_PROXIES
import log_regexps


requests.packages.urllib3.disable_warnings() 


class Validator:
    def __init__(self):
        pass

    def validate(self, sources):
        print('[*] Validating {} sources...'.format(len(sources)))
        valid_sources = Queue()
        log_validators = []

        for link in sources:
            log_validators.append(LogValidator(valid_sources, link))

        for log_validator in log_validators:
            log_validator.start()

        for log_validator in log_validators:
            log_validator.join()
            
        return [valid_sources.get() for i in range(valid_sources.qsize())]


class LogValidator(Thread):
    def __init__(self, valid_sources_queue, log_link):
        self.valid_sources_queue = valid_sources_queue
        self.log_link = log_link
        self.apache_access = re.compile(log_regexps.APACHE_ACCESS_LOG)
        self.apache_error = re.compile(log_regexps.APACHE_ERROR_LOG)
        super().__init__()

    def run(self):
        print('[*] Checking {}...'.format(self.log_link))

        try:
            response = requests.get(self.log_link, proxies=HTTP_PROXIES, verify=False)
        except requests.exceptions.ConnectionError:
            print('[-] Connection error with {}'.format(self.log_link))
            return

        try:
            decoded_content = response.content.decode('utf-8')
        except UnicodeDecodeError:
            return

        self._validate(decoded_content)

    def _validate(self, decoded_content):
        if self.apache_access.match(decoded_content):
            self.valid_sources_queue.put(
                {'link': self.log_link, 'type': 'APACHE_ACCESS'}
            )
            print('[+] Got valid APACHE_ACCESS log {}'.format(self.log_link))
        elif self.apache_error.match(decoded_content):
            self.valid_sources_queue.put(
                {'link': self.log_link, 'type': 'APACHE_ERROR'}
            )
            print('[+] Got valid APACHE_ERROR log {}'.format(self.log_link))
        return

