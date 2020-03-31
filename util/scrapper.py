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

def log(string):
    if not hasattr(report, "logfile"):
        report.logfile = open("../datasets/.report",'w')
        report.errorlog = open("../datasets/.errors",'w')
    if re.match("^ERROR:", string):
        writeln(report.errorlog,string)
    writeln(report.logfile,string)

def get_soup(URL):
    page = requests.get(URL)
    return BeautifulSoup(page.content, 'html.parser')

# START
date_today = str(datetime.today().strftime('%Y-%m-%d'))
log(str(datetime.today().strftime('%Y-%m-%d %H:%M:%S')) + "\n")

#1. Canada
#1.a. read from website
def get_canada_cases():
    log("1. Starting Canada csv fetch and operations...")
    canada_df = pd.read_csv('https://health-infobase.canada.ca/src/data/covidLive/covid19.csv')
    canada_df.drop(columns="prnameFR", inplace=True)
    canada_df.drop(columns="numprob", inplace=True)
    canada_df.drop(columns="numtested", inplace=True)
    canada_df['date'] = [ datetime.strptime(x,'%d-%m-%Y').strftime('%Y-%m-%d') for x in canada_df['date'] ]
    #canada_df.to_csv('../datasets/canada.csv')
    log("2. Completed Canada csv fetch.")

#1.b. Scrappe for Canada Tests
def get_canada_tests():
    log("3. Starting Canada test...")
    soup = get_soup('https://www.canada.ca/en/public-health/services/diseases/2019-novel-coronavirus-infection.html')
    tables = soup.find_all('table', class_='table-condensed')
    ths = tables[0].find_all('th')
    tds = tables[0].find_all('td')

    columns = ["Total number of patients tested in Canada", "Total positive", "Total negative"]

    for i in range(0,len(ths)):
        if(ths[i].text != columns[i]):
            log("ERROR: web column names don't match canada-tests.csv schema.")
            return

    if(len(tds) != 3):
        log("ERROR: web column number is different from canada-tests.csv schema.")
        return

    with open("../datasets/canada-tests.csv",'a') as ca_tests:
        writeln(ca_tests, date_today + ", " + tds[0].text.replace(",","") + ", " + tds[1].text.replace(",","") + ", " + tds[2].text.replace(",",""))

    log("4. Completed Canada test.")

#2. Ontario
#   a. cases: total number of cases can be extracted from canada site
#   b. Tests: scrappe from 'https://www.ontario.ca/page/2019-novel-coronavirus'
#        really from 'https://api.ontario.ca/api/drupal/page%2F2019-novel-coronavirus?fields=nid,field_body_beta,body'
def get_ontario_tests():
    log("5. Getting Ontario tests...")
    soup = get_soup('https://api.ontario.ca/api/drupal/page%2F2019-novel-coronavirus?fields=nid,field_body_beta,body')
    tables = soup.find_all('table')
    trs = tables[0].find_all('tr')
    # Hardcoding values of attributes with expected ones to compare in case the website changes
    attributes = ['Negative1,','Currently under investigation2,','Confirmed positive3,', 'Resolved4,', 'Deceased,', 'Total number of patients approved for COVID-19 testing to date,']
    record = date_today
    for i in range(0, len(trs)):
        tds = trs[i].find_all('td')
        if (tds[0].text != attributes[i]):
            log("ERROR: Ontario tests table on website not what expected")
            exit()
        record = records + ", " + tds[1].text.replace(",","")

    with open("../datasets/ontario-tests.csv","a") as ontario_tests:
        writeln(ontario_tests, record)

    log("6. Completed getting Ontario tests records")

#3. Alberta
#   a. cases: number of cases can be extracted from canada site
#   b. Tests: scrappe from 'https://www.alberta.ca/covid-19-alberta-data.aspx'
def get_alberta_tests():
    log("7. Getting Alberta tests...")
    soup = get_soup('https://www.alberta.ca/covid-19-alberta-data.aspx')
    table = soup.find(id='goa-grid25723').find_all(class_='goa-tableouter')[1].find_all('table')[0]
    tr = table.find_all('tr')[0]
    # Hardcoding values of attributes with expected ones to compare in case the website changes
    if ! re.match("Completed tests", tr.find_all('th')[0].text):
        log("ERROR: Alberta tests table on website not what expected")
        return
    record = date_today + ", " + tr.find_all('td')[0].text.replace(",","")

    with open("../datasets/alberta-tests.csv","a") as alberta_tests:
        writeln(alberta_tests, record)

    log("8. Completed getting Alberta tests records")

#4. BC
#   a. cases: number of cases can be extracted from canada site
#   b. Tests: scrappe from 'http://www.bccdc.ca/about/news-stories/stories/2020/information-on-novel-coronavirus'
def get_bc_tests():
    log("9. Getting BC tests...")

    soup = get_soup('http://www.bccdc.ca/about/news-stories/stories/2020/information-on-novel-coronavirus')
    div = soup.find(id='ctl00_PlaceHolderMain_SubPlaceholder_ctl07__ControlWrapper_RichHtmlField')

    div2 = div.find_all('div')
    if len(div2) == 0:
        log('ERROR: BC tests page not what expected, aborting BC tests get')
        return

    div3 = div2[0].find_all('div')
    if len(div3) == 0:
        log('ERROR: BC tests page not what expected, aborting BC tests get')
        return

    lis = div3[0].find_all('li')
    if len(lis) == 0:
        log('ERROR: BC tests page not what expected, aborting BC tests get')
        return

# IN TABLE                       # IN WEBSITE
# -----------------------------------------------------------------
# cases                          # 970 confirmed cases as of March 30. 
# recovered                      # 469 recovered in BC
# deaths                         # 19 deaths in BC
#                                # Cases by region:
# Fraser Health                  # 323 in Fraser Health
# Interior Health                # 94 in Interior Health
# Island Health                  # 67 in Island Health
# Northern Health                # 14 in Northern Health
# Vancouver Coastal Health       # 472 in Vancouver Coastal Health.
# tests                          # 42,028 tests completed.

    attributes = {}

    try:
        for li in lis:
            if re.match("^[0-9,]+[\u00A0 ]confirmed cases", li.text):
                attributes["cases"] = int(li.text[:min(li.text.find(" "), li.text.find("\u00A0"))].replace(",",""))
            elif re.match("^[0-9,]+[\u00A0 ]recovered in BC", li.text):
                attributes["recovered"] = int(li.text[:min(li.text.find(" "), li.text.find("\u00A0"))].replace(",",""))
            elif re.match("^[0-9,]+[\u00A0 ]deaths in BC", li.text):
                attributes["deaths"] = int(li.text[:min(li.text.find(" "), li.text.find("\u00A0"))].replace(",",""))
            elif re.match("^[0-9,]+[\u00A0 ]in Fraser Health", li.text):
                attributes["Fraser Health"] = int(li.text[:min(li.text.find(" "), li.text.find("\u00A0"))].replace(",",""))
            elif re.match("^[0-9,]+[\u00A0 ]in Interior Health", li.text):
                attributes["Interior Health"] = int(li.text[:min(li.text.find(" "), li.text.find("\u00A0"))].replace(",",""))
            elif re.match("^[0-9,]+[\u00A0 ]in Island Health", li.text):
                attributes["Island Health"] = int(li.text[:min(li.text.find(" "), li.text.find("\u00A0"))].replace(",",""))
            elif re.match("^[0-9,]+[\u00A0 ]in Northern Health", li.text):
                attributes["Northern Health"] = int(li.text[:min(li.text.find(" "), li.text.find("\u00A0"))].replace(",",""))
            elif re.match("^[0-9,]+[\u00A0 ]in Vancouver Coastal Health", li.text):
                attributes["Vancouver Coastal Health"] = int(li.text[:min(li.text.find(" "), li.text.find("\u00A0"))].replace(",",""))
            elif re.match("^[0-9,]+[\u00A0 ]tests completed" in li.text:
                attributes["tests"] = int(li.text[:min(li.text.find(" "), li.text.find("\u00A0"))].replace(",",""))
            elif not "Cases by region" in li.text:
                log("ERROR: BC tests page table not what expected")
                return
    except ValueError:
        log("ERROR: BC tests page doesn't have numbers where expected")
        return

    record = attributes['cases'] + ", " + attributes['recovered'] + ", " + attributes['deaths'] + ", " + attributes['Fraser Health'] + ", " + attributes['Interior Health'] + ", " + attributes['Island Health'] + ", " + attributes['Northern Health'] + ", " + attributes['Vancouver Coastal Health'] + ", " + attributes['tests']

    with open("../datasets/bc-tests.csv","a") as bc_tests:
        writeln(bc_tests, record)

    log("10. Completed getting BC tests records")
