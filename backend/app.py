import os
import time
import requests
import boto3
import logging
from flask import Flask, jsonify, request
from boto3.dynamodb.conditions import Key
from dotenv import load_dotenv

logging.basicConfig(
  filename='app.log',
  level=logging.DEBUG,
  format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
)

app = Flask(__name__)

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('indeed-jobs')

load_dotenv() # to load variables from .env file
APIFY_INDEED_KEY = os.getenv('APIFY_INDEED_KEY')

@app.route('/indeed_jobs', methods=['POST'])
def get_indeed_jobs():
  logging.info('Received request to scape jobs from Indeed API')
  try:
    api_url = f'https://api.apify.com/v2/acts/misceres~indeed-scraper/run-sync-get-dataset-items?token={APIFY_INDEED_KEY}'
    payload = request.json

    response = requests.post(api_url, json=payload)
    data = response.json()
    logging.info(f'data from first url is {data}')

    time.sleep(30)

    dataset_url= f'https://api.apify.com/v2/datasets/{data}/items?token={APIFY_INDEED_KEY}'
    result_response = requests.get(dataset_url)
    result_data = result_response.json()
    logging.info(f'this is the data from result_data - {result_data}')

    for item in result_data:
      table.put_item(Item=item)

    return jsonify(status='success', data=result_data)
  except Exception as e:
    logging.error(f'Error scraping jobs {e}')
    return jsonify(error='Failed to scrape jobs'), 500

@app.route('/', methods=['GET'])
def hello_world():
  return jsonify(message='hello world')

if __name__ == '__main__':
  port = int(os.environ.get("PORT", 3000))
  app.run(debug=True, port=port)