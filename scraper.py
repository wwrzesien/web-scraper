import requests
from bs4 import BeautifulSoup

website_page = 'https://mediamarkt.pl/rtv-i-telewizory/hifi-audio/gramofony'
headers = {'User_Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0)' +
           'Gecko/20100101 Firefox/68.0'}

source = requests.get(website_page, headers=headers).text
soup = BeautifulSoup(source, 'lxml')

# Get all cantainers data.
house_containers = soup.find_all('div', class_='m-productsBox_containerInner')

# for container in house_containers:
# Get container name.
container = house_containers[0]
name = container.find_all('p', class_='m-productsBox_name')
print(name[0].text)
# print(house_containers[0])

"""
ctrl + / -> comment multiples lines
ctrl + left click -> write simultaneously in several rows
"""
