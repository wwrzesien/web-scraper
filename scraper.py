import requests
from bs4 import BeautifulSoup

website_page = 'https://mediamarkt.pl/rtv-i-telewizory/hifi-audio/gramofony'
headers = {'User_Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0)' +
           'Gecko/20100101 Firefox/68.0'}

source = requests.get(website_page, headers=headers).text
soup = BeautifulSoup(source, 'html.parser')


def get_feature_from_line(words):
    """Extract features from line."""
    for idx, word in enumerate(words):
        if ':' in word:
            colon_pos = idx
    key = ' '.join(words[:colon_pos+1])
    value = ' '.join(words[colon_pos+1:])
    return key, value


def get_record_player_data():
    """Receive record players data from website
    and save to list od dictonaries."""
    record_players_data = []
    player_data = {}

    # Get all cantainers data.
    house_containers = soup.find_all(
        'div', class_='m-productsBox_containerInner')

    for container in house_containers:
        # Get container name.
        name = container.find_all('p', class_='m-productsBox_name')

        player_data['Name'] = name[0].get_text().strip()

        # Get features.
        house_features = container.find_all(
            'ul', class_='m-productsBox_features')
        features = house_features[0].find_all('li')

        for feature in features:
            feature_raw = feature.get_text().strip().replace('\n', '')
            key, value = get_feature_from_line(words=feature_raw.split())

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
        record_players_data.append(player_data)


get_record_player_data()
"""
ctrl + / -> comment multiples lines
ctrl + left click -> write simultaneously in several rows
"""
