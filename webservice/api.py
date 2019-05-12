from flask import Flask, Response, request
from flask_cors import CORS
from webservice.config import *
import random
import json
import re
import requests

from xbot.xbotdb import Xbotdb
from xbot.product import loadProductfromJSON

xbot_webservice = Flask(__name__)
CORS(xbot_webservice)

current_scraper = random.choice(SCRAPERS)
current_scraper_pro = random.choice(SCRAPERS_PRO)
current_api_scraper = random.choice(SCRAPERS_XBOT)

xbotdb = Xbotdb()
pro_users = ['gavaste', 'Vincent_Vegaa']


def captureURLs(text):
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    return urls


def get_scraper(user):
    global current_scraper
    global current_scraper_pro
    global current_api_scraper

    if user in pro_users:
        return current_scraper_pro
    elif user == 'XBOT_API':
        return current_api_scraper
    else:
        return current_scraper


def update_current_scraper(user):
    global current_scraper
    global current_scraper_pro
    global current_api_scraper

    if user in pro_users:
        current_scraper_pro = random.choice(list(set(SCRAPERS_PRO) - set([current_scraper_pro])))

        # Avoid duplicated Dynos running
        current_api_scraper = random.choice(list(set(SCRAPERS_XBOT) - set([current_api_scraper])))

    elif user == 'XBOT_API':
        current_scraper_pro = random.choice(list(set(SCRAPERS_PRO) - set([current_scraper_pro])))
        current_api_scraper = random.choice(list(set(SCRAPERS_XBOT) - set([current_api_scraper])))
    else:
        current_scraper = random.choice(list(set(SCRAPERS) - set([current_scraper])))

    return 0


@xbot_webservice.route("/")
def index():
    return 'xbot_proxy'


def scrape(url, user):
    scraper = get_scraper(user)

    print(f'Using {scraper}')

    if url == '':
        return {'Error': 'Parameter url not found'}, 400
    else:
        r = requests.post(f'{scraper}{SCRAPER_ENDPOINT}', json={'url': url})
        print(r.json())
        if r.json().get('short_description') is None:
            update_current_scraper(user)
            r = requests.post(f'{scraper}{SCRAPER_ENDPOINT}', json={'url': url})

        return {'data': r.json(), 'status': 200}


@xbot_webservice.route('/api/scrape', methods=['POST'])
def redirect_scrape():
    print('-------------------------------------------')
    url = request.json.get('url')
    user = request.json.get('user') or None
    print('URL='+url)
    print('user='+user)
    scraped = scrape(url, user)
    print('***********************************************')
    return Response(json.dumps(scraped['data']), status=scraped['status'], mimetype='application/json')


@xbot_webservice.route('/api/newoffer', methods=['POST'])
def new_offer():
    if request.content_type != 'application/json':
        return Response(json.dumps({'Error': 'Content-Type must be application/json'}), status=400, mimetype='application/json')

    payload = request.json
    message = payload.get('message')
    origin = payload.get('origin')

    if message is None:
        error_message = '"message" field is mandatory, try with {"message": "hello world", "origin": "me"}'
        return Response(json.dumps({'Error': error_message}), status=400, mimetype='application/json')

    urls = captureURLs(message)
    offers = []
    for url in urls:
        print(url)
        scraped = scrape(url, user='XBOT_API')
        if scraped['status'] == 200:
            offers.append(scraped['data'])
        print(origin)

    for offer in offers:
        # Save in Mongo
        product = loadProductfromJSON(offer)
        if product.is_completed:
            xbotdb.insert_product(product, telegram_name='XBOT_API')

    return Response(json.dumps(offers), status=200, mimetype='application/json')


if __name__ == '__main__':
    xbot_webservice.run(debug=True)
