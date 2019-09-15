import logging
from scraper import Scraper

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
logger.addHandler(handler)

website_page = 'https://mediamarkt.pl/rtv-i-telewizory/hifi-audio/gramofony'
headers = {'User_Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0)' +
           'Gecko/20100101 Firefox/68.0'}


def main():
    scraper = Scraper(website_page=website_page, headers=headers)

    scraper.get_record_player_data()
    print(scraper.record_players_data)


if __name__ == '__main__':
    main()
    logger.info('Record player data was extracted from the website.')
