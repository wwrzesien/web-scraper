import logging
from scraper import Scraper
import sqlite as sq

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
logger.addHandler(handler)

website_page = 'https://mediamarkt.pl/rtv-i-telewizory/hifi-audio/gramofony'
headers = {'User_Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0)' +
           'Gecko/20100101 Firefox/68.0'}


def main():
    scraper = Scraper(website_page=website_page, headers=headers)

    # Get data from the website.
    scraper.get_record_player_data()

    # Save data to database.
    data = scraper.record_players_data
    print(data)
    for row in data:
        # print(row)
        sq.insert_record_player(row)
    # print(data[0])
    # Close database.
    sq.conn.close()


if __name__ == '__main__':
    main()
    logger.info('Record player data was extracted from the website.')
