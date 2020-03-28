import requests
from bs4 import BeautifulSoup

URL = 'https://www.canada.ca/en/public-health/services/diseases/2019-novel-coronavirus-infection.html'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

tables = soup.find_all('table', class_='table-condensed')

for table in tables:
    print(table)
