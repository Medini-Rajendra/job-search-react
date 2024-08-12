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
app.logger.setLevel(logging.DEBUG)

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('indeed-jobs')

load_dotenv() # to load variables from .env file
APIFY_INDEED_KEY = os.getenv('APIFY_INDEED_KEY')

@app.route('/indeed_jobs', methods=['POST'])
def get_indeed_jobs():
  app.logger.info('Received request to scape jobs from Indeed API')
  try:
    api_url = f'https://api.apify.com/v2/acts/misceres~indeed-scraper/run-sync-get-dataset-items?token={APIFY_INDEED_KEY}'
    payload = request.json

    response = requests.post(api_url, json=payload)
    data = response.json()

    for item in data:
      try:
        prep_data = {
          'job_id': item['id'],
          'jobtitle': item['positionName'],
          'salary': item['salary'],
          'company': item['company'],
          'location': item['location'],
          'jobtype': item['jobType'],
          'applylink': item['externalApplyLink']
        }
        table.put_item(Item=prep_data)
      except KeyError as e:
        app.logger.error(f'Missing expected field in data: {e}')
      except Exception as e:
        app.logger.error(f'Error inserting item into DynamoDB: {e}')

    return jsonify(status='success', data=data)
  except Exception as e:
    app.logger.error(f'Error scraping jobs {e}')
    return jsonify(error='Failed to scrape jobs'), 500

@app.route('/', methods=['GET'])
def hello_world():
  return jsonify(message='hello world')

if __name__ == '__main__':
  port = int(os.environ.get("PORT", 3000))
  app.run(debug=True, port=port)