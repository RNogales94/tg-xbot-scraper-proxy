from flask import Flask, Response, request
from flask_cors import CORS
from webservice.config import SCRAPERS, SCRAPER_ENDPOINT
import random
import json
from requests import get as get_url

xbot_webservice = Flask(__name__)
CORS(xbot_webservice)
current_scraper = random.choice(SCRAPERS)


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
        return Response(json.dumps(r.json()), status=r.status_code, mimetype='application/json')


if __name__ == '__main__':
    xbot_webservice.run(debug=True)
