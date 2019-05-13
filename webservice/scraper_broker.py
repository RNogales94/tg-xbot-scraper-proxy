





import random
import requests
import os

from webservice.singleton import Singleton
from webservice.url_utils import get_app_name
from webservice.config import SCRAPERS, SCRAPERS_PRO, SCRAPERS_XBOT, pro_users


@Singleton
class ScraperBroker:
    def __init__(self):
        self.current_scraper = random.choice(SCRAPERS)
        self.current_scraper_pro = random.choice(SCRAPERS_PRO)
        self.current_api_scraper = random.choice(SCRAPERS_XBOT)

    def get_scraper(self, user):
        self.current_scraper
        self.current_scraper_pro
        self.current_api_scraper

        if user in pro_users:
            return self.current_scraper_pro
        elif user == 'XBOT_API':
            return self.current_api_scraper
        else:
            return self.current_scraper

    def restart_scraper(self, scraper_address):
        r = requests.delete(f'https://api.heroku.com/apps/{get_app_name(scraper_address)}/dynos/web.1', headers={
            'Content-Type': 'application/json',
            'Accept': 'application/vnd.heroku+json; version=3',
        }, auth=(os.environ['HEROKU_SCRAPERS_USER'], os.environ['HEROKU_SCRAPERS_PASS']))
        print(f'Restarting {get_app_name(scraper_address)}')
        print(f'{r.content}')
        return r.status_code

    def update_current_scraper(self, user):
        self.current_scraper
        self.current_scraper_pro
        self.current_api_scraper

        if user in pro_users:
            self.restart_scraper(self.current_scraper_pro)

            self.current_scraper_pro = random.choice(list(set(SCRAPERS_PRO) - set([self.current_scraper_pro])))
            # Avoid duplicated Dynos running
            self.current_api_scraper = self.current_scraper_pro

        elif user == 'XBOT_API':
            self.restart_scraper(self.current_api_scraper)
            current_scraper_pro = random.choice(list(set(SCRAPERS_PRO) - set([self.current_scraper_pro])))
            self.current_api_scraper = current_scraper_pro
        else:
            self.current_scraper = random.choice(list(set(SCRAPERS) - set([self.current_scraper])))

        return 0

