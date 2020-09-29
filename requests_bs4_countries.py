from bs4 import BeautifulSoup
import requests

BASE_URL = "https://en.wikipedia.org/wiki/List_of_national_capitals_in_alphabetical_order"

capitals_countries = []

html = requests.get(BASE_URL).text
soup = BeautifulSoup(html, "html.parser")
country_table = soup.find('table', {"class: wikitable sortable jquery-tablesorter"})

for row in country_table.find_all('tr'):
    cols = row.find_all('td')

    if len(cols) == 3:
        capitals_countries.append((cols[0].text.strip(), cols[1].text.strip()))

for capital, country in capitals_countries:
    print('{:35} {}'.format(capital, country))