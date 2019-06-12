import re
import requests
import urllib


def captureURLs(text):
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    return urls


def expand_url(url):
    session = requests.Session()  # so connections are recycled
    resp = session.head(url, allow_redirects=True)
    return resp.url


def get_app_name(scraper_address):
    return urllib.parse.urlparse(scraper_address).hostname.split('.')[0]


def is_amazon(url):
    try:
        url = expand_url(url)
    except requests.exceptions.ConnectionError:
        print(f'Exception: Connection refused {url}')
        return False
    return 'amazon' in urllib.parse.urlparse(url).hostname


def is_aliexpress(url):
    try:
        url = expand_url(url)
    except requests.exceptions.ConnectionError:
        print(f'Exception: Connection refused {url}')
        return False
    return 'aliexpress' in urllib.parse.urlparse(url).hostname
