import chromedriver_autoinstaller
from selenium import webdriver
from bs4 import BeautifulSoup
import requests

'''chromedriver_autoinstaller.install()
driver = webdriver.Chrome()

driver.get('https://www.worten.pt/produtos/consola-nintendo-switch-v2-6994947')
html = driver.page_source'''



html = requests.get("https://www.worten.pt/produtos/consola-nintendo-switch-v2-6994947").content

soup = BeautifulSoup(html, 'html.parser')
'''print(soup.prettify())'''

import scrapy
from scrapy_splash import SplashRequest

class WortenSpider(scrapy.Spider):
    name = 'worten_spider'
    start_urls = ['https://www.worten.pt/produtos/consola-nintendo-switch-v2-6994947']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, endpoint='render.html', args={'wait': 3})

    def parse(self, response):
        # Extract data from the rendered HTML
        product_name = response.css('h1[itemprop="name"]::text').get()
        price = response.css('span[data-price]::attr(data-price)').get()

        print(f'Product Name: {product_name}, Price: {price}')


'''
product_title = soup.find('div', 'product-header__title').text
product_price = soup.find('span', 'price__value').find('span', 'integer').text + ',' + soup.find('span', 'price__value').find('span', 'decimal').text
print(product_title, product_price)'''