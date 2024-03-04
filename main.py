import json
import os
import asyncio
from typing import List, Union

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess, CrawlerRunner
import uvicorn
from tutorial.tutorial.spiders.__init__ import LeroySpider, WortenSpider
from scrapy.utils.project import get_project_settings
settings = get_project_settings()

from pydantic import BaseModel

class CrawlRequest(BaseModel):
    urls: List[str]



app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/products/")
def trigger_crawl(request: CrawlRequest):
    # Get the list of URLs from the request JSON
    import pdb; pdb.set_trace()

    urls = request.urls

    # Check if the 'urls' key is present in the JSON
    if not urls:
        return JSONResponse(content={'error': 'No URLs provided in the request.'}, status_code=400)

    # Make requests for each URL using Scrapy and collect the results
    results = run_scrapy_crawl(urls)

    return JSONResponse(content={'status': 200, 'message': 'Requests completed successfully!', 'results': results}, status_code=200)


def run_scrapy_crawl(urls):
    results = []

    # Specify the path to your JSON file
    json_file_path = 'output.json'

    # Open the file in write mode and clear its contents by writing an empty JSON object
    with open(json_file_path, 'w') as json_file:
        json.dump({}, json_file)

    # Create a Scrapy process
    process = CrawlerProcess(get_project_settings())
    
    for url in urls:
        # Run the spider for each URL
        if 'worten.pt' in url:
            process.crawl(WortenSpider, url=url)
        elif 'leroymerlin.pt' in url:
            process.crawl(LeroySpider, url=url)
        else:
            continue

    # Start the process and block until all spiders are finished
    process.start()

    output_data = read_output_json()
    if output_data:
        results.append({'data': output_data})
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

if __name__ == "__main__":
    try:
        asyncio.run(uvicorn.run(app, host="0.0.0.0", port=8000))
    except Exception as e:
        print(f"An error occurred: {e}")