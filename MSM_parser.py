import bs4
from requests import utils, get
import requests
from bs4 import BeautifulSoup
import xml.dom.minidom
import re
import logging

headers = {
    "accept": "*/*",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.160 YaBrowser/22.5.1.985 Yowser/2.5 Safari/537.36"
}

def get_location(url):
    responce = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(responce.text, 'lxml')
    ip = soup.find("div", class_="ip").text.strip() # strip - обрезает пробелы
    location = soup.find("div", class_="value-country").text.strip()
    print(f"IP: {ip}\nLocation: {location}")

def main():
    get_location(url="https://2ip.ru/")

if __name__ == "__main__":
    main()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('Ozon')

class Client:

    def __init__(self):
        self.session = requests.Session()
        self.session_headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.160 YaBrowser/22.5.2.615 Yowser/2.5 Safari/537.36",
                                "Accept-Language": 'ru'}

    def load_page(self):
        url = "https://www.wildberries.ru/catalog/0/search.aspx?sort=popular&search=%D1%85%D0%BB%D0%BE%D0%BF%D1%8C%D1%8F+%D0%BE%D0%B2%D1%81%D1%8F%D0%BD%D1%8B%D0%B5#c81887951"
        res = self.session.get(url)
        # res.raise_for_status() # Возвращает код 200 при успехе
        return res.text # Возвращаем страницу в формате html

    def parse_page(self, text: str):
        soup = bs4.BeautifulSoup(text, 'lxml')
        container = soup.find_all('div', class_="product-card__wrapper")
        result = []
        # for x in container:
        #     result.append(str(x))
        # pattern = ''
        # href = re.search(pattern, result[0])
        # result.extend(href.find_all(text=re.search(r'href=[\'"]?([^\'" >]+)', href)))
        return container

client = Client()
print(client.load_page())
print(client.parse_page(client.load_page()))


