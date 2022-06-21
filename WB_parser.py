# Все импорты
import requests
from datetime import datetime
import json
from bs4 import BeautifulSoup
import bs4
from selenium import webdriver # Это типа импорт селениума
from selenium.webdriver.common.by import By
import pandas as pd

# щас импортируем работу селениума с выпадающими списками
from selenium.webdriver.support.select import Select

import time


# chrome version: 102.0.5005.115

page_urls = [
    'https://www.wildberries.ru/catalog/0/search.aspx?page=1&sort=popular&search=хлопья+овсяные',
    'https://www.wildberries.ru/catalog/0/search.aspx?page=2&sort=popular&search=хлопья+овсяные',
    'https://www.wildberries.ru/catalog/0/search.aspx?page=3&sort=popular&search=хлопья+овсяные',
    'https://www.wildberries.ru/catalog/0/search.aspx?page=4&sort=popular&search=хлопья+овсяные',
    'https://www.wildberries.ru/catalog/0/search.aspx?page=5&sort=popular&search=хлопья+овсяные',
    'https://www.wildberries.ru/catalog/0/search.aspx?page=6&sort=popular&search=хлопья+овсяные',
    'https://www.wildberries.ru/catalog/0/search.aspx?page=7&sort=popular&search=хлопья+овсяные',
    'https://www.wildberries.ru/catalog/0/search.aspx?page=8&sort=popular&search=хлопья+овсяные',
]

page_url = 'https://www.wildberries.ru/catalog/0/search.aspx?sort=popular&search=%D1%85%D0%BB%D0%BE%D0%BF%D1%8C%D1%8F+%D0%BE%D0%B2%D1%81%D1%8F%D0%BD%D1%8B%D0%B5#c81887951&utm_source=vkentryprofit&click_id=v1_496824492'

json_urls = [
    'https://search.wb.ru/exactmatch/ru/common/v4/search?appType=1&couponsGeo=12,3,18,15,21&curr=rub&dest=-1029256,-102269,-1278703,-1255563&emp=0&lang=ru&locale=ru&pricemarginCoeff=1.0&query=хлопья%20овсяные&reg=0&regions=68,64,83,4,38,80,33,70,82,86,75,30,69,22,66,31,48,1,40,71&resultset=catalog&sort=popular&spp=0&stores=117673,122258,122259,125238,125239,125240,6159,507,3158,117501,120602,120762,6158,121709,124731,159402,2737,130744,117986,1733,686,132043,161812,1193', # page 1
    'https://search.wb.ru/exactmatch/ru/common/v4/search?appType=1&couponsGeo=12,3,18,15,21&curr=rub&dest=-1029256,-102269,-1278703,-1255563&emp=0&lang=ru&locale=ru&page=2&pricemarginCoeff=1.0&query=хлопья%20овсяные&reg=0&regions=68,64,83,4,38,80,33,70,82,86,75,30,69,22,66,31,48,1,40,71&resultset=catalog&sort=popular&spp=0', # page 2
    'https://search.wb.ru/exactmatch/ru/common/v4/search?appType=1&couponsGeo=12,3,18,15,21&curr=rub&dest=-1029256,-102269,-1278703,-1255563&emp=0&lang=ru&locale=ru&page=5&pricemarginCoeff=1.0&query=%D1%85%D0%BB%D0%BE%D0%BF%D1%8C%D1%8F%20%D0%BE%D0%B2%D1%81%D1%8F%D0%BD%D1%8B%D0%B5&reg=0&regions=68,64,83,4,38,80,33,70,82,86,75,30,69,22,66,31,48,1,40,71&resultset=catalog&sort=popular&spp=0', # page 4
]

json_urls_2 = [
    'https://search.wb.ru/exactmatch/ru/common/v4/search?appType=1&couponsGeo=12,3,18,15,21&curr=rub&dest=-1029256,-102269,-1278703,-1255563&emp=0&lang=ru&locale=ru&pricemarginCoeff=1.0&query=%D1%85%D0%BB%D0%BE%D0%BF%D1%8C%D1%8F%20%D0%BE%D0%B2%D1%81%D1%8F%D0%BD%D1%8B%D0%B5&reg=0&regions=68,64,83,4,38,80,33,70,82,86,75,30,69,22,66,31,48,1,40,71&resultset=filters&spp=0', # page 3
    'https://search.wb.ru/exactmatch/ru/common/v4/search?appType=1&couponsGeo=12,3,18,15,21&curr=rub&dest=-1029256,-102269,-1278703,-1255563&emp=0&lang=ru&locale=ru&pricemarginCoeff=1.0&query=%D1%85%D0%BB%D0%BE%D0%BF%D1%8C%D1%8F%20%D0%BE%D0%B2%D1%81%D1%8F%D0%BD%D1%8B%D0%B5&reg=0&regions=68,64,83,4,38,80,33,70,82,86,75,30,69,22,66,31,48,1,40,71&resultset=filters&spp=0', # page 5
    'https://search.wb.ru/exactmatch/ru/common/v4/search?appType=1&couponsGeo=12,3,18,15,21&curr=rub&dest=-1029256,-102269,-1278703,-1255563&emp=0&lang=ru&locale=ru&pricemarginCoeff=1.0&query=%D1%85%D0%BB%D0%BE%D0%BF%D1%8C%D1%8F%20%D0%BE%D0%B2%D1%81%D1%8F%D0%BD%D1%8B%D0%B5&reg=0&regions=68,64,83,4,38,80,33,70,82,86,75,30,69,22,66,31,48,1,40,71&resultset=filters&spp=0', # page 6
    'https://search.wb.ru/exactmatch/ru/common/v4/search?appType=1&couponsGeo=12,3,18,15,21&curr=rub&dest=-1029256,-102269,-1278703,-1255563&emp=0&lang=ru&locale=ru&pricemarginCoeff=1.0&query=%D1%85%D0%BB%D0%BE%D0%BF%D1%8C%D1%8F%20%D0%BE%D0%B2%D1%81%D1%8F%D0%BD%D1%8B%D0%B5&reg=0&regions=68,64,83,4,38,80,33,70,82,86,75,30,69,22,66,31,48,1,40,71&resultset=filters&spp=0', # page 7
    'https://search.wb.ru/exactmatch/ru/common/v4/search?appType=1&couponsGeo=12,3,18,15,21&curr=rub&dest=-1029256,-102269,-1278703,-1255563&emp=0&lang=ru&locale=ru&pricemarginCoeff=1.0&query=%D1%85%D0%BB%D0%BE%D0%BF%D1%8C%D1%8F%20%D0%BE%D0%B2%D1%81%D1%8F%D0%BD%D1%8B%D0%B5&reg=0&regions=68,64,83,4,38,80,33,70,82,86,75,30,69,22,66,31,48,1,40,71&resultset=filters&spp=0', # page 8
]

# dick = requests.get('https://search.wb.ru/exactmatch/ru/common/v4/search?appType=1&couponsGeo=12,3,18,15,21&curr=rub&dest=-1029256,-102269,-1278703,-1255563&emp=0&lang=ru&locale=ru&pricemarginCoeff=1.0&query=%D1%85%D0%BB%D0%BE%D0%BF%D1%8C%D1%8F%20%D0%BE%D0%B2%D1%81%D1%8F%D0%BD%D1%8B%D0%B5&reg=0&regions=68,64,83,4,38,80,33,70,82,86,75,30,69,22,66,31,48,1,40,71&resultset=filters&spp=0')
# with open(f'хуй.json', 'w', encoding='utf-8') as f:
#     json.dump(dick.json(), f, indent=4, ensure_ascii=False)

name_list = []
brand_list = []

def collect_data(url, n):
    # Получаю ответ на запрос
    responce = requests.get(url=url)
    # Добавляю время, чтобы файл не перезаписывался, а создавался новый
    t_date = datetime.now().strftime('%d_%m_%Y')
    # Открываю файл для записи json-формата
    with open(f'data_{t_date}_{n}.json', 'w', encoding='utf-8') as file:
        json.dump(responce.json(), file, indent=4, ensure_ascii=False)

    data = responce.json()['data']
    prod = data["products"]
    for one_name in prod:
        name = one_name['name']
        brand = one_name['brand']
        name_list.append(name)
        brand_list.append(brand)
        # print(f'{name}, {brand}')
    return None

def collect_data_two(url, n):
    responce = requests.get(url)
    t_date = datetime.now().strftime('%d_%m_%Y')
    with open(f'data_{t_date}_{n}.json', 'w', encoding='utf-8') as file:
        json.dump(responce.json(), file, indent=4, ensure_ascii=False)

    data = responce.json()['data']['filters']
    name = responce.json()['metadata']['name']
    brand = data[1]['items']
    for brand_name in brand:
        name_list.append(name)
        brand_list.append(brand_name['name'])


collect_data_two(json_urls_2[3], 16)

def selenium_parse():
    pass



def main():
    count = 1
    count_two = 4

    for json_page in json_urls:
        collect_data(json_page, count)
        count = count + 1

    for json_page in json_urls_2:
        collect_data_two(json_page, count_two)
        count_two = count_two + 1

    selenium_parse()

if __name__ == '__main__':
    main()

# Так можно открыть хром с помощью selenium
# Слэши эуранируются (то есть два обратных слеша)
# browser = webdriver.Chrome(executable_path='C:\\Users\\Максим\\Desktop\\WB_parser\\chromedriver.exe')
# browser.maximize_window() # Сразу открывается на весь экран
# # Получаем какую-то ссылку
# browser.get(url)
# # Поиск элемента
# href = browser.find_element(By.XPATH, value='')
# print(f'{href.text}, хуй')

driver = webdriver.Chrome()

try:
    driver.get(url=page_urls[0])
    # driver.maximize_window()
    # time.sleep(2) # Чтобы браузер сразу не закрылся
    frame = driver.find_element(By.XPATH, '//*[@id="c12117076"]/div/a')
    # with open('selenium_file.txt', 'w') as f:
    #     f.write(page)
except Exception as ex:
    print('Пошел нахуй')
finally:
    driver.close()
    driver.quit()

# print(name_list.__sizeof__())
# print(brand_list.__sizeof__())

table = pd.DataFrame({'name': name_list,
         'brand name': brand_list})

date = datetime.now().strftime('%d_%m_%Y')

table.to_excel(f'table{date}.xlsx')

