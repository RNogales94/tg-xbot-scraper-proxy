from flask import Flask, Response, request
from flask_cors import CORS
from webservice.config import SCRAPERS, SCRAPER_ENDPOINT
import random
import json
import re
import requests

xbot_webservice = Flask(__name__)
CORS(xbot_webservice)
current_scraper = random.choice(SCRAPERS)


def captureURLs(text):
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    return urls


@xbot_webservice.route("/")
def index():
    return 'xbot_proxy'


def scrape(url):
    global current_scraper
    print(f'Using {current_scraper}')

    if url == '':
        return {'Error': 'Parameter url not found'}, 400
    else:
        r = requests.post(f'{current_scraper}{SCRAPER_ENDPOINT}', json={'url': url})
        if r.json().get('short_description') is None:
            current_scraper = random.choice(list(set(SCRAPERS) - set([current_scraper])))
            r = requests.post(f'{current_scraper}{SCRAPER_ENDPOINT}', json={'url': url})

        return {'data': r.json(), 'status': 200}


@xbot_webservice.route('/api/scrape', methods=['POST'])
def redirect_scrape():
    url = request.json.get('url')
    scraped = scrape(url)
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
        scraped = scrape(url)
        if scraped['status'] == 200:
            offers.append(scraped['data'])
        print(origin)

    return Response(json.dumps(offers), status=200, mimetype='application/json')




if __name__ == '__main__':
    xbot_webservice.run(debug=True)
