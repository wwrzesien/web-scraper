import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
logger.addHandler(handler)


class Scraper:
    def __init__(self, website_page, headers):
        self.website_page = website_page
        self.headers = headers

    def get_record_player_data(self):
        """Receive record players data from to website
        and save it as a list of dictonaries."""
        player_data = {
            'Nazwa': '',
            'Typ_napędu': '',
            'Typ_ramienia': '',
            'Regulacja_obrotów': '',
            'Sterowanie': '',
            'USB': '',
            'Cena': ''
        }
        self.record_players_data = []

        source = requests.get(self.website_page, headers=self.headers).text
        self.soup = BeautifulSoup(source, 'html.parser')

        # Get all cantainers data.
        self.house_containers = self.soup.find_all(
            'div', class_='m-productsBox_containerInner')

        for container in self.house_containers:
            # Get container name.
            house_name = container.find_all('p', class_='m-productsBox_name')

            words = house_name[0].get_text().split()
            name = self.get_record_player_name(words)
            if name == '':
                continue
            else:
                player_data['Nazwa'] = name

            # Get features.
            house_features = container.find_all(
                'ul', class_='m-productsBox_features')
            features = house_features[0].find_all('li')

            for feature in features:
                feature_raw = feature.get_text().strip().replace('\n', '')
                key, value = self.get_feature_from_line(
                    words=feature_raw.split())
                if key in player_data.keys():
                    player_data[key] = value

            # Get price.
            house_prices = container.find_all(
                'div', class_='m-priceBox_price')
            prices_raw = house_prices[0].find_all('span')

            price_list = []
            for price_raw in prices_raw:
                if price_raw['class'][1][-1].isdigit():
                    price_list.append(price_raw['class'][1][-1])

            player_data['Cena'] = ''.join(price_list)

            # Append record player data to database.
            self.record_players_data.append(dict(player_data))

    def get_feature_from_line(self, words):
        """Extract features from list of words."""
        for idx, word in enumerate(words):
            if ':' in word:
                colon_pos = idx
        key = ' '.join(words[:colon_pos+1]).replace(':', '')
        key = key.replace(' ', '_')
        value = ' '.join(words[colon_pos+1:])
        return key, value

    def get_record_player_name(self, words):
        """Extract reord players' name from list of words."""
        sign_pos = len(words)
        for idx, word in enumerate(words):
            if '+' in word:
                sign_pos = idx
        words.remove('Gramofon')
        name = ' '.join(words[:sign_pos-1])
        return name


"""
ctrl + / -> comment multiples lines
ctrl + left click -> write simultaneously in several rows
"""
