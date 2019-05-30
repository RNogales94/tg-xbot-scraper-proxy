import os

# BASE URL FOR SCRAPERS

SCRAPER_ENDPOINT = '/api/scrape'

pro_users = ['gavaste', 'Vincent_Vegaa', 'RNogales', 'Fkillo', 'DraCarYsssss']


SCRAPERS = [
    'https://xbot-scraper01.herokuapp.com/',
    'https://xbot-scraper02.herokuapp.com/',
    'https://xbot-scraper03.herokuapp.com/',
]

code = ''

if os.environ['HEROKU_SCRAPERS_USER'] == 'katerina.lopatkova95@gmail.com':
    code = 'c'
elif os.environ['HEROKU_SCRAPERS_USER'] == 'info@xbot.dev':
    code = 'b'

SCRAPERS_PRO = [
    f'https://xbot-scraper01{code}.herokuapp.com/',
    f'https://xbot-scraper02{code}.herokuapp.com/',
    f'https://xbot-scraper03{code}.herokuapp.com/',
]

SCRAPERS_XBOT = [
    f'https://xbot-scraper01{code}.herokuapp.com/',
    f'https://xbot-scraper02{code}.herokuapp.com/',
    f'https://xbot-scraper03{code}.herokuapp.com/',
]
