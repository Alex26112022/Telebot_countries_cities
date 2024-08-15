import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from fake_headers import Headers

load_dotenv()

# API_TOKEN = os.getenv('API_TOKEN')
# headers = {
#     'Authorization': f'Bearer {API_TOKEN}',
#     'Accept-Language': 'ru'
# }
#
# search_words = 'search-regions'
# params = {
#     'searchTerm': 'Москва'
# }
#
# URL = f'https://data-api.oxilor.com/rest/{search_words}'

URL = 'https://infourok.ru/spisok-stran-i-ih-stolic-5710813.html'

headers = {
    'user-agent': Headers(os="win", headers=True).generate()['User-Agent']
}

params = None

response = requests.get(URL, headers=headers)

soup = BeautifulSoup(response.text, 'lxml')

table = soup.find('table', attrs={'class': 'MsoNormalTable'})
cities_countries = table.find_all('tr')

for el in cities_countries[1:]:
    countries = el.find('p', attrs={'class': 'MsoNormal'}).text
    countries_url = el.find('a')['href']
    cities = el.find('p', attrs={'class': 'MsoNormal', 'align': 'center'}).text
    # print(f'{countries}: {cities}\n{countries_url}')

    detail_response = requests.get(countries_url, headers=headers)
    detail_soup = BeautifulSoup(detail_response.text, 'lxml')
    detail_table = detail_soup.find('div', attrs={'class': 'info'})
    country_details = detail_table.find_all('dd')

    try:
        area = country_details[3].contents[1].strip()
        people = country_details[4].contents[1].strip()
        official_language = country_details[8].text
        valuta = country_details[9].text
        phone_code = country_details[10].text
        image = f'http://ostranah.ru/{detail_soup.find_all('img')[1]['src']}'
    except IndexError:
        area = country_details[4].contents[1].strip()
        people = country_details[5].contents[1].strip()
        official_language = country_details[9].text
        valuta = country_details[10].text
        phone_code = country_details[11].text
        image = f'http://ostranah.ru/{detail_soup.find_all('img')[1]['src']}'

    print(
        f'{countries}: {cities}\nArea: {area}\nPopulation: {people}\nOfficial language: {official_language}\nValuta: {valuta}\nPhone code: {phone_code}\n{countries_url}\n{image}\n')
