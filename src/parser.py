import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
from tqdm import tqdm


def parse():
    """ Парсинг стран и городов. """
    full_info = []
    URL = 'https://infourok.ru/spisok-stran-i-ih-stolic-5710813.html'

    headers = {
        'user-agent': Headers(os="win", headers=True).generate()['User-Agent']
    }

    response = requests.get(URL, headers=headers)

    soup = BeautifulSoup(response.text, 'lxml')

    table = soup.find('table', attrs={'class': 'MsoNormalTable'})
    cities_countries = table.find_all('tr')

    for el in tqdm(cities_countries[1:]):
        countries = el.find('p', attrs={'class': 'MsoNormal'}).text
        countries_url = el.find('a')['href']
        cities = el.find('p',
                         attrs={'class': 'MsoNormal', 'align': 'center'}).text

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
            image = f'http://ostranah.ru/{detail_soup.find_all('img')[1]['src']}'  # noqa
        except IndexError:
            area = country_details[4].contents[1].strip()
            people = country_details[5].contents[1].strip()
            official_language = country_details[9].text
            valuta = country_details[10].text
            phone_code = country_details[11].text
            image = f'http://ostranah.ru/{detail_soup.find_all('img')[1]['src']}'  # noqa

        info = (countries, cities, area, people, official_language,
                valuta, phone_code, countries_url, image)
        full_info.append(info)
    return full_info


if __name__ == '__main__':
    parse()
