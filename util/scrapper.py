import requests
from bs4 import BeautifulSoup

from datetime import datetime

#Table of Contents:
#1. Canada
#   a. cases
#       read from 'https://health-infobase.canada.ca/src/data/covidLive/covid19.csv'
#   b. tests
#       scrappe from 'https://www.canada.ca/en/public-health/services/diseases/2019-novel-coronavirus-infection.html'
#2. Ontario
#   a. cases
#       _ from _
#       * Ontario website no longer publishing case by case data, total number of cases can be extracted from canada site
#   b. Tests
#       scrappe from 'https://www.ontario.ca/page/2019-novel-coronavirus'
#3. Alberta
#   a. cases
#       number of cases can be extracted from canada site
#   b. Tests
#       scrappe from 'https://www.alberta.ca/covid-19-alberta-data.aspx'
#4. BC
#   a. cases
#       number of cases can be extracted from canada site
#   b. Tests
#       scrappe from 'http://www.bccdc.ca/about/news-stories/stories/2020/information-on-novel-coronavirus'
#4. Quebec
#   a. cases
#       number of cases can be extracted from canada site
#   b. Tests
#       scrappe from 'https://msss.gouv.qc.ca/professionnels/maladies-infectieuses/coronavirus-2019-ncov/'
#           In FRENCH
#4. Nunavut
#   a. cases
#       number of cases can be extracted from canada site
#   b. Tests
#       scrappe from 'https://www.gov.nu.ca/health/information/covid-19-novel-coronavirus'
#5. North West Territoris
#   a. cases
#       number of cases can be extracted from canada site
#   b. Tests
#       scrappe from 'https://www.hss.gov.nt.ca/en/services/coronavirus-disease-covid-19'
#6. Yukon
#   a. cases
#       number of cases can be extracted from canada site
#   b. Tests
#       scrappe from 'https://yukon.ca/covid-19'
#7. Prince Edward Island
#   a. cases
#       number of cases can be extracted from canada site
#   b. Tests
#       scrappe from 'https://www.princeedwardisland.ca/en/topic/covid-19'
#8. Nova Scotia
#   a. cases
#       number of cases can be extracted from canada site
#   b. Tests
#       scrappe from 'https://novascotia.ca/coronavirus/'
#9. New Brunswick
#   a. cases
#       number of cases can be extracted from canada site
#   b. Tests
#       scrappe from 'https://www2.gnb.ca/content/gnb/en/departments/ocmoh/cdc/content/respiratory_diseases/coronavirus.html'
#10. Newfoundland and Labrador
#   a. cases
#       number of cases can be extracted from canada site
#   b. Tests
#       scrappe from 'https://www.gov.nl.ca/covid-19/'
#11. Manitoba
#   a. cases
#       number of cases can be extracted from canada site
#   b. Tests
#       scrappe from 'https://www.gov.mb.ca/covid19/'
#12. Saskatchewan
#   a. cases
#       number of cases can be extracted from canada site
#   b. Tests
#       scrappe from 'https://www.saskatchewan.ca/government/health-care-administration-and-provider-resources/treatment-procedures-and-guidelines/emerging-public-health-issues/2019-novel-coronavirus/cases-and-risk-of-covid-19-in-saskatchewan'

#13. Worldwide data
#   a. confirmed cases
#       read csv from 'https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_global.csv&filename=time_series_covid19_confirmed_global.csv'
#   b. deaths
#       read csv from 'https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_deaths_global.csv&filename=time_series_covid19_deaths_global.csv'
#   c. recovered
#       read csv from 'https://data.humdata.org/hxlproxy/api/data-  preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_recovered_global.csv&filename=time_series_covid19_recovered_global.csv'
#
#14.Tests numbers for select countries
#   a. Canada
#       DONE in point one above
#   b. US
#       scrappe from 'http://covidtracking.com/api/states/daily.csv'
#   c. South Korea
#       scrappe from 'https://www.cdc.go.kr/board/board.es?mid=&bid=0030'
#   d. Italy
#       scrappe from 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale-latest.csv'
#   e. Spain
#       scrappe from ''
#   f. Iran
#       scrappe from ''
#   g. Germany
#       scrappe from ''
#   h. France
#       scrappe from ''
#   i. UK
#       scrappe from 'https://www.gov.uk/guidance/coronavirus-covid-19-information-for-the-public'
#   j. Singapore
#       scrappe from ''
#   k. Japon
#       scrappe from ''

# START
def writeln(file, string):
    file.write(string + "\n")

report = open("../datasets/.report",'w')
date_today = datetime.today().strftime('%Y-%m-%d')
writeln(report, date_today + "\n")

#1. Canada
#1.b. Scrappe for Canada Tests
writeln(report,"1. Starting Canada test...")
URL = 'https://www.canada.ca/en/public-health/services/diseases/2019-novel-coronavirus-infection.html'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
tables = soup.find_all('table', class_='table-condensed')
ths = tables[0].find_all('th')
tds = tables[0].find_all('td')

columns = ["Total number of patients tested in Canada", "Total positive", "Total negative"]

for i in range(0,len(ths)):
    if(ths[i].text != columns[i]):
        writeln(report, "ERROR: web column names don't match canada-tests.csv schema.")
        exit()

if(len(tds) != 3):
    writeln(report, "ERROR: web column number is different from canada-tests.csv schema.")
    exit()

with open("../datasets/canada-tests.csv",'a') as ca_tests:
    writeln(ca_tests, date_today + ", " + tds[0].text.replace(",","") + ", " + tds[1].text.replace(",","") + ", " + tds[2].text.replace(",",""))

writeln(report, "2. Completed Canada test.")
