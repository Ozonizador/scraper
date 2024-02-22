import json
import os
import subprocess
from typing import Union

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from scrapy.crawler import CrawlerProcess
from tutorial.tutorial.spiders.__init__ import WortenSpider


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/products/")
def trigger_crawl(request: Request):
    # Get the list of URLs from the request JSON
    request_data = request.json()
    urls = request_data.get('urls', [])

    # Check if the 'urls' key is present in the JSON
    if not urls:
        return JSONResponse(content={'error': 'No URLs provided in the request.'}, status_code=400)

    # Make requests for each URL using Scrapy and collect the results
    results = run_scrapy_crawl(urls)

    return JSONResponse(content={'status': 200, 'message': 'Requests completed successfully!', 'results': results}, status_code=200)


def run_scrapy_crawl(urls):
    results = []

    for url in urls:
        process = CrawlerProcess()
        process.crawl(WortenSpider, url=url)
        process.start()

        # Access items collected by the spider after the crawl
        output_data = getattr(WortenSpider, 'collected_items', None)

        if output_data:
            results.append({'url': url, 'data': output_data})
        else:
            results.append({'url': url, 'error': 'Empty output from Scrapy crawl.'})

    return results

def read_output_json():
    
    # Define the path to the output.json file
    output_file_path = os.path.join(os.getcwd(), 'output.json')

    # Check if the file exists
    if os.path.exists(output_file_path):
        # Read the contents of the output.json file
        try:
            with open(output_file_path, 'r') as f:
                output_data = json.load(f)
            return output_data
        except json.JSONDecodeError as e:
            return {'error': f"Error decoding JSON: {e}"}
    else:
        return {'error': 'output.json file not found.'}

if __name__ == '__main__':
    # Run the app on localhost:5000
    app.run(debug=True)