from flask import Flask, jsonify, request
import requests
import boto3
from boto3.dynamodb.conditions import Key

app = Flask(__name__)

dynamodb = boto3.resource('dynamodb', region='us-east-1')
table = dynamodb.Table('indeed-jobs')

@app.route('/indeed_jobs', methods=['POST'])
def get_indeed_jobs():
  api_url = 'https://api.apify.com/v2/acts/misceres~indeed-scraper/run-sync-get-dataset-items?token=apify_api_csYwh9WSdz0JyyPP4IAArx50PEIoVW2QHrd3'
  payload = request.json

  response = requests.post(api_url, json=payload)
  data = response.json()

  for item in data:
    table.put_item(Item=item)

  return jsonify(status='success', data=data)

if __name__ == '__main__':
  app.run(debug=True)