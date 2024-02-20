from flask import Flask, jsonify, request
import subprocess
import os
import json
import time
import requests  # Import the requests library

app = Flask(__name__)

# Define a route to trigger the Scrapy crawl with a list of URLs
@app.route('/api/crawl', methods=['POST'])
def trigger_crawl():
    # Get the list of URLs from the request JSON
    request_data = request.get_json()
    urls = request_data.get('urls', [])

    # Check if the 'urls' key is present in the JSON
    if not urls:
        return jsonify({'error': 'No URLs provided in the request.'}), 400

    # Make requests for each URL using Scrapy and collect the results
    results = run_scrapy_crawl(urls)

    return jsonify({'status': 200, 'message': 'Requests completed successfully!','results': results}), 200

def run_scrapy_crawl(urls):
    # Replace 'myproject' with your actual Scrapy project name
    project_name = 'tutorial'
    
    # Replace 'worten_spider' with your actual spider name
    spider_name = 'worten_spider'
    
    # Navigate to the Scrapy project folder
    project_folder = os.path.join(os.getcwd(), project_name)
    print(f"Navigating to {project_folder}")
    os.chdir(project_folder)

    # Prepare the results list
    results = []

    for url in urls:
        # Run the Scrapy crawl command for each URL
        cmd = f"scrapy crawl {spider_name} -a url={url}"
        print(f"Running command: {cmd}")

        try:
            # Capture the output of the command
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)

            # Check if the output is not empty
            if read_output_json():
                # Parse the JSON result
                output_data = read_output_json()
                results.append({'url': url, 'data': output_data})
            else:
                results.append({'url': url, 'error': 'Empty output from Scrapy crawl.'})
        except subprocess.CalledProcessError as e:
            results.append({'url': url, 'error': f"Error: {e}"})

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
