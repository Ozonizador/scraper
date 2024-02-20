import json
import scrapy
from scrapy_splash import SplashRequest

class WortenSpider(scrapy.Spider):
    name = 'worten_spider'
    start_urls = ['https://www.worten.pt/produtos/consola-nintendo-switch-v2-6994947']
    output_filename = 'output.json'  # Fixed filename
    scraped_data = []

    def start_requests(self):
        for url in self.start_urls:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
            yield SplashRequest(url, self.parse, endpoint='render.html', args={'wait': 3}, headers=headers)

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
        output = {'product_name': product_name, 'price': price}
        filename = self.save_to_file(output)

        # Save the results to a temporary list
        output = {'product_name': product_name, 'price': price}
        self.scraped_data.append(output)

        self.log(f'Results saved to {filename}')

    def save_to_file(self, output):
        with open(self.output_filename, 'w') as f:
            json.dump(output, f)

        return self.output_filename

    def closed(self, reason):
        self.log(f'Spider closed: {reason}')

        # Return 200 status code upon successful completion
        return {'status': 200, 'data': self.scraped_data}
