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

        source = requests.get(website_page, headers=headers).text
        self.soup = BeautifulSoup(source, 'html.parser')

    def get_record_player_data(self):
        """Receive record players data from website
        and save to list od dictonaries."""
        self.record_players_data = []
        player_data = {}

        # Get all cantainers data.
        self.house_containers = self.soup.find_all(
            'div', class_='m-productsBox_containerInner')

        for container in self.house_containers:
            # Get container name.
            name = container.find_all('p', class_='m-productsBox_name')

            player_data['Name'] = name[0].get_text().strip()

            # Get features.
            house_features = container.find_all(
                'ul', class_='m-productsBox_features')
            features = house_features[0].find_all('li')

            for feature in features:
                feature_raw = feature.get_text().strip().replace('\n', '')
                key, value = self.get_feature_from_line(
                    words=feature_raw.split())

                player_data[key] = value

            # Get price.
            house_prices = container.find_all(
                'div', class_='m-priceBox_price')
            prices_raw = house_prices[0].find_all('span')

            price_list = []
            for price_raw in prices_raw:
                if price_raw['class'][1][-1].isdigit():
                    price_list.append(price_raw['class'][1][-1])

            player_data['Price'] = ''.join(price_list)

            # Append record player data to database.
            self.record_players_data.append(player_data)

    def get_feature_from_line(self, words):
        """Extract features from line."""
        for idx, word in enumerate(words):
            if ':' in word:
                colon_pos = idx
        key = ' '.join(words[:colon_pos+1])
        value = ' '.join(words[colon_pos+1:])
        return key, value


"""
ctrl + / -> comment multiples lines
ctrl + left click -> write simultaneously in several rows
"""
