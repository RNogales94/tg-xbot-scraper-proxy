from flask import Flask, Response, request
from flask_cors import CORS
from webservice.config import SCRAPERS, SCRAPER_ENDPOINT
import random
import json
import re
from requests import get as get_url

xbot_webservice = Flask(__name__)
CORS(xbot_webservice)
current_scraper = random.choice(SCRAPERS)

def captureURLs(text):
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    return urls


@xbot_webservice.route("/")
def index():
    return 'xbot_proxy'


@xbot_webservice.route('/api/scrape')
def redirect_scrape():
    global current_scraper
    print(f'Using {current_scraper}')
    url = request.args.get('url') or ''

    if url == '':
        return Response(json.dumps({'Error': 'Parameter url not found'}), status=400, mimetype='application/json')
    else:
        r = get_url(f'{current_scraper}{SCRAPER_ENDPOINT}?url={url}')
        if r.json().get('short_description') is None:
            current_scraper = random.choice(list(set(SCRAPERS) - set([current_scraper])))
            r = get_url(f'{current_scraper}{SCRAPER_ENDPOINT}?url={url}')

        return Response(json.dumps(r.json()), status=r.status_code, mimetype='application/json')


@xbot_webservice.route('/api/newoffer', methods=['POST'])
def new_offer():
    payload = request.json
    message = payload.get('message')
    origin = payload.get('origin')

    urls = captureURLs(message)
    for url in urls:
        print(url)
        print(origin)

    dummy = {
        "short_description": "Samsung EVO Plus - Tarjeta de Memoria microSD de 128 GB con Adaptador SD, 100 MB/s, U3, Color Rojo y Blanco",
        "description": "Tarjeta de memoria microSD Samsung EVO PLUS 128Gb MB-MC128GAEU + adaptador SD incluido en el blíster. 100Mb/s de lectura y 90 Mb/de escritura. Controladora U3.",
        "features": "Lectura 100 Mb/s\nEscritura 90 Mb/s\nControladora U3\n› Ver más detalles",
        "standard_price": "EUR 88,99",
        "end_date": None,
        "price": "EUR 23,92",
        "url": "https://www.amazon.es/gp/product/B06XFHQGB9?pf_rd_p=44ae21af-cb43-440e-bcab-82e6a5324e39",
        "image_url": "https://images-na.ssl-images-amazon.com/images/I/61EA%2B6P9I0L._SL1150_.jpg",
        "size": None
    }
    return Response(json.dumps(dummy), status=200, mimetype='application/json')


if __name__ == '__main__':
    xbot_webservice.run(debug=True)
