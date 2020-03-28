import requests
from bs4 import BeautifulSoup

from datetime import datetime

report = open("../datasets/.report",'w')
date_today = datetime.today().strftime('%Y-%m-%d')
report.write(date_today + "\n")

# Scrappe for Canada Tests
report.write("Starting Canada test...")
URL = 'https://www.canada.ca/en/public-health/services/diseases/2019-novel-coronavirus-infection.html'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
tables = soup.find_all('table', class_='table-condensed')
ths = tables[0].find_all('th')
tds = tables[0].find_all('td')

columns = ["Total number of patients tested in Canada", "Total positive", "Total negative"]

for i in range(0,len(ths)):
    if(ths[i].text != columns[i]):
        report.write("ERROR: web column names don't match canada-tests.csv schema.")
        exit()

if(len(ths) != 3):
    report.write("ERROR: web column number is different from canada-tests.csv schema.")
    exit()

with open("../datasets/canada-tests.csv",'a') as ca_tests:
    ca_tests.write(date_today + ", " + )

report.write("Completed Canada test.")
