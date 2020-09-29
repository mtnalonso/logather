import requests

from startpage import Startpage
from tor_proxies import HTTP_PROXIES


def main():
    print('Using ip: {}'.format(get_tor_ip()))

    sp = Startpage()
    sources = sp.get_sources(50)

    from pprint import pprint
    pprint(sources)
    print(len(sources))


def get_tor_ip():
    response = requests.get('http://httpbin.org/ip', proxies=HTTP_PROXIES)
    return response.text



if __name__ == '__main__':
    main()
