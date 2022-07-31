# TODO парсинг данных интернет-магазина

import requests
from bs4 import BeautifulSoup
from time import sleep

headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0'}


def download(url):# функция для скачивания картинок в папку
    resp = requests.get(url, stream=True)
    r = open('C:\\Users\\Asus\\PycharmProjects\\parser\\pic\\' + url.split('/')[-1], 'wb')
    for value in resp.iter_content(1024 * 1024):
        r.write(value)
    r.close()


def get_url():
    for page in range(1, 8):
        url = f'https://scrapingclub.com/exercise/list_basic/?page={page}'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        data = soup.find_all('div', class_="col-lg-4 col-md-6 mb-4")  # весь текст с тегом, карточка товара
        # print(data)
        for i in data:
            card_url = 'https://scrapingclub.com' + i.find('a').get('href')
            yield card_url


def array():
    for card_url in get_url():
        response = requests.get(card_url, headers=headers)
        sleep(3)  # задержка между запросами, защита от блокировки
        soup = BeautifulSoup(response.text, 'lxml')
        data = soup.find('div', class_="card mt-4 my-4")
        name = data.find('h3', class_="card-title").text
        price = data.find('h4').text
        text_card = data.find('p', class_="card-text").text
        url_image = 'https://scrapingclub.com' + data.find('img', class_="card-img-top img-fluid").get('src')
        download(url_image)
        yield name, price, text_card, url_image
