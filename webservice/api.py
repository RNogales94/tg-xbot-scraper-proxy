from flask import Flask, Response, request
from flask_cors import CORS
import json
import requests

from xbot.xbotdb import Xbotdb
from xbot.product import loadProductfromJSON

from webservice.scraper_broker import ScraperBroker
from webservice.config import SCRAPER_ENDPOINT
from webservice.url_utils import is_amazon, captureURLs, is_aliexpress


xbot_webservice = Flask(__name__)
CORS(xbot_webservice)

scrape_broker = ScraperBroker()
xbotdb = Xbotdb()


@xbot_webservice.route("/")
def index():
    return 'xbot_proxy'


def scrape(url, user):
    scraper = scrape_broker.get_scraper(user)

    print(f'Using {scraper}')

    if url == '':
        return {'data': {'Error': 'Parameter url not found'}, 'status': 400}
    else:
        r = requests.post(f'{scraper}{SCRAPER_ENDPOINT}', json={'url': url})
        print(r.status_code)
        try:
            data = r.json()
        except:
            print(f"Scraper {scraper} cannot scrape {url}")
            return {'data': {}, 'status': 501}

        if r.json().get('short_description') is None:
            scrape_broker.update_current_scraper(user)
            r = requests.post(f'{scraper}{SCRAPER_ENDPOINT}', json={'url': url})

        return {'data': r.json(), 'status': 200}


@xbot_webservice.route('/api/scrape', methods=['POST'])
def redirect_scrape():
    print('-------------------------------------------')
    url = request.json.get('url')
    user = request.json.get('user') or None
    print('URL='+url)
    print('user='+user)
    if is_amazon(url) or is_aliexpress(url):
        scraped = scrape(url, user)
        response = json.dumps(scraped['data'])
        status = scraped['status']
    else:
        response = {}
        status = 400
    print('***********************************************')
    return Response(response, status=status, mimetype='application/json')


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
        if is_amazon(url) or is_aliexpress(url):
            scraped = scrape(url, 'XBOT_API')
            status = scraped['status']
        else:
            status = 400

        if status == 200:
            offers.append(scraped['data'])
        print(origin)

    for offer in offers:
        # Save in Mongo
        product = loadProductfromJSON(offer)
        if product.is_completed:
            xbotdb.insert_product(product, telegram_name='XBOT_API')
    print({'Message': f'Document inserted in mongo ({len(offers)})'})
    return Response(json.dumps(offers), status=200, mimetype='application/json')


if __name__ == '__main__':
    xbot_webservice.run(debug=True)
