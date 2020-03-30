import requests
from bs4 import BeautifulSoup
import re

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
#13. Quebec
#   a. cases
#       number of cases can be extracted from canada site
#   b. Tests
#       scrappe from 'https://msss.gouv.qc.ca/professionnels/maladies-infectieuses/coronavirus-2019-ncov/'
#           In FRENCH
#14. Nunavut
#   a. cases
#       number of cases can be extracted from canada site
#   b. Tests
#       scrappe from 'https://www.gov.nu.ca/health/information/covid-19-novel-coronavirus'

#15. Worldwide data
#   a. confirmed cases
#       read csv from 'https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_global.csv&filename=time_series_covid19_confirmed_global.csv'
#   b. deaths
#       read csv from 'https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_deaths_global.csv&filename=time_series_covid19_deaths_global.csv'
#   c. recovered
#       read csv from 'https://data.humdata.org/hxlproxy/api/data-  preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_recovered_global.csv&filename=time_series_covid19_recovered_global.csv'
#
#16. Tests numbers for select countries
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
#17. Joins
#   a. join each province tests with canada on province and date
#   b. join each countries tests with Worldwide confirmed data on country and date
#18. Calculations
#   a. calculate cases and tests per 10K population for countries, Canada Provinces, US States
#19. to save:
#   a. canada with cases per day and tests per day for each province

#Function definitions:
def writeln(file, string):
    file.write(string + "\n")

def get_soup(URL):
    page = requests.get(URL)
    return BeautifulSoup(page.content, 'html.parser')

# START
report = open("../datasets/.report",'w')
date_today = str(datetime.today().strftime('%Y-%m-%d'))
writeln(report, date_today + "\n")

#1. Canada
#1.a. read from website
writeln(report,"1. Starting Canada csv fetch and operations...")
canada_df = pd.read_csv('https://health-infobase.canada.ca/src/data/covidLive/covid19.csv')
canada_df.drop(columns="prnameFR", inplace=True)
canada_df.drop(columns="numprob", inplace=True)
canada_df.drop(columns="numtested", inplace=True)
canada_df['date'] = [ datetime.strptime(x,'%d-%m-%Y').strftime('%Y-%m-%d') for x in canada_df['date'] ]
#canada_df.to_csv('../datasets/canada.csv')
writeln(report, "2. Completed Canada csv fetch.")

#1.b. Scrappe for Canada Tests
writeln(report,"3. Starting Canada test...")
soup = get_soup('https://www.canada.ca/en/public-health/services/diseases/2019-novel-coronavirus-infection.html')
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

writeln(report, "4. Completed Canada test.")

#2. Ontario
#   a. cases: total number of cases can be extracted from canada site
#   b. Tests: scrappe from 'https://www.ontario.ca/page/2019-novel-coronavirus'
#        really from 'https://api.ontario.ca/api/drupal/page%2F2019-novel-coronavirus?fields=nid,field_body_beta,body'
writeln(report, "5. Getting Ontario tests...")
soup = get_soup('https://api.ontario.ca/api/drupal/page%2F2019-novel-coronavirus?fields=nid,field_body_beta,body')
tables = soup.find_all('table')
trs = tables[0].find_all('tr')
# Hardcoding values of attributes with expected ones to compare in case the website changes
attributes = ['Negative1,','Currently under investigation2,','Confirmed positive3,', 'Resolved4,', 'Deceased,', 'Total number of patients approved for COVID-19 testing to date,']
record = date_today
for i in range(0, len(trs)):
    tds = trs[i].find_all('td')
    if (tds[0].text != attributes[i]):
        writeln(report, "ERROR: Ontario tests table on website not what expected")
        exit()
    record = records + ", " + tds[1].text.replace(",","")

with open("../datasets/ontario-tests.csv","a") as ontario_tests:
    writeln(ontario_tests, record)

writeln(report, "6. Completed getting Ontario tests records")

#3. Alberta
#   a. cases: number of cases can be extracted from canada site
#   b. Tests: scrappe from 'https://www.alberta.ca/covid-19-alberta-data.aspx'
writeln(report, "7. Getting Alberta tests...")
soup = get_soup('https://www.alberta.ca/covid-19-alberta-data.aspx')
table = soup.find(id='goa-grid25723').find_all(class_='goa-tableouter')[1].find_all('table')[0]
tr = table.find_all('tr')[0]
# Hardcoding values of attributes with expected ones to compare in case the website changes
if ! re.match("Completed tests", tr.find_all('th')[0].text):
    writeln(report, "ERROR: Alberta tests table on website not what expected")
    exit()
record = date_today + ", " + tr.find_all('td')[0].text.replace(",","")

with open("../datasets/alberta-tests.csv","a") as alberta_tests:
    writeln(alberta_tests, record)

writeln(report, "8. Completed getting Alberta tests records")

#4. BC
#   a. cases: number of cases can be extracted from canada site
#   b. Tests: scrappe from 'http://www.bccdc.ca/about/news-stories/stories/2020/information-on-novel-coronavirus'
writeln(report, "9. Getting BC tests...")

# WIP: NEED TO FIX COMMENTED OUT CODE TO BE USED FOR BC DATA
#soup = get_soup('https://www.alberta.ca/covid-19-alberta-data.aspx')
# table = soup.find(id='goa-grid25723').find_all(class_='goa-tableouter')[1].find_all('table')[0]
# tr = table.find_all('tr')[0]
# Hardcoding values of attributes with expected ones to compare in case the website changes
# if ! re.match("Completed tests", tr.find_all('th')[0].text):
#     writeln(report, "ERROR: Alberta tests table on website not what expected")
#     exit()
# record = date_today + ", " + tr.find_all('td')[0].text.replace(",","")
#
# with open("../datasets/alberta-tests.csv","a") as alberta_tests:
#     writeln(alberta_tests, record)

writeln(report, "10. Completed getting BC tests records")
