import scrapy
from scrapy_splash import SplashRequest
import json
import requests
from dotenv import load_dotenv
import os
from scrapy import signals
from w3lib.http import basic_auth_header

# Load environment variables from .env file
load_dotenv()

class WortenSpider(scrapy.Spider):
    name = 'worten_spider'
    output_filename = 'output.json'  # Fixed filename
    scraped_data = []

    def __init__(self, *args, **kwargs):
        super(WortenSpider, self).__init__(*args, **kwargs)
        self.start_url = kwargs.get('url', '')

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        
        # Access the value of SMARTPROXY_URL
        username = os.getenv("username")
        password = os.getenv("password")
        yield scrapy.Request(url=self.start_url, callback=self.parse,
                meta={'proxy': f'https://{username}:{password}@dc.smartproxy.com:10000'},
                headers=headers
            )

    def parse(self, response):
        # Extract data from the rendered HTML
        product_name = response.css('div.product-header__title span::text').get()
        integer_part = response.css('span.price__value span.value .integer::text').get()
        separator_part = response.css('span.price__value span.value .separator::text').get()
        decimal_part = response.css('span.price__value span.value .decimal::text').get()

        # Combine the parts to form the complete price
        price = f"{integer_part or ''}{separator_part or ''}{decimal_part or ''}"

        # Print the results to the console
        self.log(f'Product Name: {product_name}, Price: {price}')

        # Save the results to a fixed JSON file
        output = {'status': 200, 'data': {'competitor': 'worten','product_name': product_name, 'price': price, 'size': str(len(response.body))}}
        self.scraped_data.append(output)

    def closed(self, reason):
        self.log(f'Spider closed: {reason}')

        # Save the results to the output file
        with open(self.output_filename, 'w') as f:
            json.dump(self.scraped_data, f)

        self.log(f'Results saved to {self.output_filename}')


class LeroySpider(scrapy.Spider): 
    name = "leroy_spider"
    output_filename = 'output.json'  # Fixed filename
    scraped_data = []

    def __init__(self, *args, **kwargs):
        super(LeroySpider, self).__init__(*args, **kwargs)
        # Get the 'url' argument from the command line, or set a default URL
        self.start_url = kwargs.get('url', '')
        
    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        
        # Access the value of SMARTPROXY_URL
        username = os.getenv("username")
        password = os.getenv("password")
        yield scrapy.Request(url=self.start_url, callback=self.parse,
                meta={'proxy': f'https://{username}:{password}@dc.smartproxy.com:10000'},
                headers=headers
            )

    def parse(self, response):
        # Extract data from the rendered HTML
        product_name = response.css('h1.l-product-detail-presentation__title::text').get()
        price = response.css('div.kl-price .js-main-price::text').get()
        original_price = response.css('div.kl-price span.km-price__from-without-offer::text').get()

        self.logger.info('test: ' + response)

        # Print the results to the console
        self.log(f'Product Name: {product_name}, Price: {price}')

        # Save the results to a fixed JSON file
        output = {'status': 200, 'data': {'competitor':'leroy','product_name': product_name, 'price': price, 'original_price': original_price, 'size': str(len(response.body))}}
        # output = {'status': response.status_code, 'reason': response.reason}
        self.scraped_data.append(output)

    def closed(self, reason):
        self.log(f'Spider closed: {reason}')

        # Save the results to the output file
        with open(self.output_filename, 'w') as f:
            json.dump(self.scraped_data, f)

        self.log(f'Results saved to {self.output_filename}')


class BricoDepotSpider(scrapy.Spider):
    name = "brico_depot_spider"
    output_filename = 'output.json'  # Fixed filename
    scraped_data = []

    def __init__(self, *args, **kwargs):
        with open(self.output_filename, 'r') as f:
            self.scraped_data = json.load(f)

        super(BricoDepotSpider, self).__init__(*args, **kwargs)
        # Get the 'url' argument from the command line, or set a default URL
        self.start_url = kwargs.get('url', '')

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        
        
        # Access the value of SMARTPROXY_URL
        username = os.getenv("username")
        password = os.getenv("password")
        yield scrapy.Request(url=self.start_url, callback=self.parse,
                meta={'proxy': f'https://{username}:{password}@dc.smartproxy.com:10000'},
                headers=headers
            )

    def parse(self, response):
        if response.status_code == 200:
            # Extract data from the rendered HTML
            product_name = response.css('h1.l-product-detail-presentation__title::text').get()
            price = response.css('div.kl-price .js-main-price::text').get()
            original_price = response.css('div.kl-price span.km-price__from-without-offer::text').get()

            # Print the results to the console
            self.log(f'Product Name: {product_name}, Price: {price}')

            # Save the results to a fixed JSON file
            output = {'status': 200, 'data': {'competitor':'leroy','product_name': product_name, 'price': price, 'original_price': original_price, 'size': str(len(response.body))}}
        else:
            output = {'status': response.status_code, 'reason': response.reason}
        self.scraped_data.append(output)

    def closed(self, reason):
        self.log(f'Spider closed: {reason}')

        # Save the results to the output file
        with open(self.output_filename, 'w') as f:
            json.dump(self.scraped_data, f)

        self.log(f'Results saved to {self.output_filename}')


class IpTester(scrapy.Spider):
    name = "ip_tester"
    output_filename = 'output.json'  # Fixed filename
    scraped_data = []

    def __init__(self, *args, **kwargs):
        with open(self.output_filename, 'r') as f:
            self.scraped_data = json.load(f)

        super(IpTester, self).__init__(*args, **kwargs)
        # Get the 'url' argument from the command line, or
        # set a default URL
        self.start_url = kwargs.get('url', '')

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
        }

        # Access the value of SMARTPROXY_URL
        username = os.getenv("username")
        password = os.getenv("password")
        yield scrapy.Request(url=self.start_url, callback=self.parse,
                meta={'proxy': f'https://{username}:{password}@dc.smartproxy.com:10000'},
                headers=headers,
            )

    def parse(self, response):
        # Extract data from the rendered HTML
        ip = response.css('#client-ipv4 span.flag-text::text').get()

        # Print the results to the console
        self.log(f'Ip: {ip}')

        # Save the results to a fixed JSON file
        output = {'status': 200, 'data': {'ip': ip}}

        self.log(output)

    def closed(self, reason):
        self.log(f'Spider closed: {reason}')

        # Save the results to the output file
        with open(self.output_filename, 'w') as f:
            json.dump(self.scraped_data, f)

        self.log(f'Results saved to {self.output_filename}')
