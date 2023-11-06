import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from openpyxl import load_workbook
import time

def site_scrap():
    wb = load_workbook("table.xlsx")
    ws = wb["data"]
    ua = UserAgent()
    nextURL = 'https://www.proff.no/søk-etter-bransje/entreprenører/I:441/?q=Entreprenører'
    count = 0
    dont_email = 0
    while nextURL:
        response = requests.get(url=nextURL, headers={'user-agent': f'{ua.random}'})
        soup = BeautifulSoup(response.text, 'lxml')
        search_containers = soup.find('div', class_='search-container-wrap').find_all('div', class_='search-container')
        search_block_wraps = soup.find_all('a', class_='addax addax-cs_hl_hit_company_name_click')
        nextHR = soup.find('li', class_='next').find('a', class_='arrow ssproff-right')
        nextURL = 'https://www.proff.no' + nextHR.get('href') if nextHR else None
        links = []
        for search_container in search_containers:
            entreprenorer = 'https://www.proff.no' + search_container.find('a', class_='addax addax-cs_hl_hit_company_name_click').get('href')
            links.append(entreprenorer)
        for link in links:
            response = requests.get(url=link, headers={'user-agent': f'{ua.random}'})
            soup = BeautifulSoup(response.text, 'lxml')
            try:
                email = soup.find('a', class_='addax addax-cs_ip_email_click').find('span').text
                header = soup.find('div', class_='header-wrap clear').find('h1').text
                ws.append([header, email])
            except Exception as _ex:
                if dont_email > 58:
                    nextHR = None
                    nextURL = None
                    break
                else:
                    dont_email += 1
                    continue
            finally:
                if count > 300:
                    time.sleep(10)
                    count = 0
                else:
                    count += 1
    wb.save("table.xlsx")
    wb.close()

def main():
    site_scrap()

if __name__ == "__main__":
    main()