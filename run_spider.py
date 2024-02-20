from flask import Flask, jsonify
import subprocess
import os
import json
import time

app = Flask(__name__)

# Define a route to trigger the Scrapy crawl
@app.route('/api/crawl', methods=['GET'])
def trigger_crawl():
    # Run the Scrapy crawl command and capture the output
    result = run_scrapy_crawl()
    return jsonify(result)

    # Check if the crawl returned a 200 status code
    if result.get('status') == 200:
        time.sleep(2)
        # Read the contents of the output.json file
        output_json = read_output_json()
        return jsonify({'message': 'Crawl completed successfully!', 'output': output_json}), 200
    else:
        return jsonify({'message': 'Crawl failed or returned a non-200 status code.', 'output': result}), 500

def run_scrapy_crawl():
    # Replace 'myproject' with your actual Scrapy project name
    project_name = 'tutorial'
    
    # Replace 'worten_spider' with your actual spider name
    spider_name = 'worten_spider'
    
    # Navigate to the Scrapy project folder
    project_folder = os.path.join(os.getcwd(), project_name)
    print(f"Navigating to {project_folder}")
    os.chdir(project_folder)

    # Run the Scrapy crawl command using subprocess
    cmd = f"scrapy crawl {spider_name}"
    print(f"Running command: {cmd}")

    try:
        # Capture the output of the command
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        print(result, 'result.stdout')

        # Check if the output is not empty
        if result.stdout.strip():
            # Parse the JSON result
            result_json = json.loads(result.stdout)
            return result_json
        else:
            return {'status': 500, 'error': 'Empty output from Scrapy crawl.'}
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return {'status': 500, 'error': f"Error: {e}"}

def read_output_json():
    # Replace 'myproject' with your actual Scrapy project name
    project_name = 'tutorial'
    
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
