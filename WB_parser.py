# Все импорты
import requests
from datetime import datetime
import json
from selenium import webdriver # Это типа импорт селениума
from selenium.webdriver.common.by import By
import pandas as pd
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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




headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru,en;q=0.9',
    'cache-control': 'max-age=0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.160 YaBrowser/22.5.2.615 Yowser/2.5 Safari/537.36'
}


firm_name = []
href_list = []
info_list = []
firm_name_done = []




def parse_page_one():
    driver = webdriver.Chrome()
    driver.get(url = page_urls[0])
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="c81887951"]'))
    )
    el = driver.find_element(By.XPATH, '//*[@id="catalog-content"]/div/div').find_elements(By.CLASS_NAME, 'product-card.j-card-item.j-good-for-listing-event')

    for element in el:
        info = element.find_element(By.CLASS_NAME, 'product-card__wrapper')
        a_tag = element.find_element(By.CLASS_NAME, 'product-card__wrapper').find_element(By.TAG_NAME, 'a')
        href = a_tag.get_attribute('href')
        href_list.append(href)
        info_list.append(info.text)

    el_two = driver.find_element(By.XPATH, '//*[@id="catalog-content"]/div/div').find_elements(By.CLASS_NAME, 'product-card.j-card-item')
    for element in el_two:
        info_two = element.find_element(By.CLASS_NAME, 'product-card__wrapper')
        a_tag_two = element.find_element(By.CLASS_NAME, 'product-card__wrapper').find_element(By.TAG_NAME, 'a')
        href_two = a_tag_two.get_attribute('href')
        href_list.append(href_two)
        info_list.append(info_two.text)
    date = datetime.now().strftime('%d_%m_%Y')

    pattern = r'(\w+\s)?\w+\s/'
    i = 1


    for el in info_list:
        result = re.search(pattern, el)
        if result == None:
            result = 'Мистраль..'
            firm_name.append(result)
            continue
        firm_name.append(result[0])

    for name in firm_name:
        name = re.sub(r'\s/', '', name)
        firm_name_done.append(name)

    with open(f'hrefs_{date}.txt', 'w', encoding='utf-8') as f:
        for el in href_list:
            f.write(f'{el}\n')
    if date == '23_06_2022':
        selenium_table = pd.DataFrame({'name': 'Хлопья овсяные',
                              'brand name': firm_name_done,
                              'href': href_list
                                })
        selenium_table.to_excel(f'another_table{date}.xlsx')




def main():
    count = 1
    count_two = 4
    now_date = datetime.now().strftime('%d_%m_%Y')
    if now_date == '21_06_2022':
        for json_page in json_urls:
            collect_data(json_page, count)
            count = count + 1

        for json_page in json_urls_2:
            collect_data_two(json_page, count_two)
            count_two = count_two + 1

    parse_page_one()




if __name__ == '__main__':
    main()

# table = pd.DataFrame({'name': name_list,
#          'brand name': brand_list})
#
# date = datetime.now().strftime('%d_%m_%Y')
#
# table.to_excel(f'table{date}.xlsx')



