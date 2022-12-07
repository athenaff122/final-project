import requests
from bs4 import BeautifulSoup
import json

def write_json(filepath, data, encoding='utf-8'):

    with open(filepath, 'w', encoding=encoding) as file_obj:
        json.dump(data, file_obj)
# BASE_URL = 'https://www.si.umich.edu'
# COURSES_PATH = '/programs/courses'

## Make the soup for the Courses page
forbes_page_url = "https://www.forbes.com/lists/global2000/?sh=1d4699995ac0"
response = requests.get(forbes_page_url)
print(response)
soup = BeautifulSoup(response.text, 'html.parser')
company_listing_parent = soup.find('div', class_='table-row-group')
company_listing_divs = company_listing_parent.find_all('a', recursive=False)

scrapping={}

for i in range(len(company_listing_divs)):
    company={}
    company_name=company_listing_divs[i].find('div', class_='organizationName second table-cell name').string
    scrapping[company_name]={}
    country=company_listing_divs[i].find('div', class_='country table-cell country').string
    scrapping[company_name]["country"]=country
    sales=company_listing_divs[i].find('div', class_='revenue table-cell sales').string
    scrapping[company_name]["sales"]=sales
    profit=company_listing_divs[i].find('div', class_='profits table-cell profit').string
    scrapping[company_name]["profit"]=profit
    asset=company_listing_divs[i].find('div', class_='assets table-cell assets').string
    scrapping[company_name]["asset"]=asset
    mkt_value=company_listing_divs[i].find('div', class_='marketValue table-cell market value').string
    scrapping[company_name]["market value"]=mkt_value
# print(scrapping)
scrapping_json=json.dumps(scrapping)
print(type(scrapping_json))
write_json('scrapping.json', scrapping_json)


