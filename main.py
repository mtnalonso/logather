import requests

from startpage import Startpage
from tor_proxies import HTTP_PROXIES
from validator import Validator


def main():
    print('Using ip: {}'.format(get_tor_ip()))

    sp = Startpage()
    sources = sp.get_sources(50)
    
    validator = Validator()
    valid_sources = validator.validate(sources)

    for source in valid_sources:
        print(source)


def get_tor_ip():
    response = requests.get('http://httpbin.org/ip', proxies=HTTP_PROXIES)
    return response.text


if __name__ == '__main__':
    main()
