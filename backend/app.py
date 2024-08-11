import os
from flask import Flask, jsonify, request
import requests
import boto3
from boto3.dynamodb.conditions import Key
from dotenv import load_dotenv

app = Flask(__name__)

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('indeed-jobs')

load_dotenv() # to load variables from .env file
APIFY_INDEED_KEY = os.getenv('APIFY_INDEED_KEY')

@app.route('/indeed_jobs', methods=['POST'])
def get_indeed_jobs():
  api_url = 'https://api.apify.com/v2/acts/misceres~indeed-scraper/run-sync-get-dataset-items?token={APIFY_INDEED_KEY}'
  payload = request.json

  response = requests.post(api_url, json=payload)
  data = response.json()

  for item in data:
    table.put_item(Item=item)

  return jsonify(status='success', data=data)

@app.route('/', methods=['GET'])
def hello_world():
  return jsonify(message='hello world')

if __name__ == '__main__':
  port = int(os.environ.get("PORT", 3000))
  app.run(debug=True, port=port)