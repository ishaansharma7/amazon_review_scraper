from utils.es_utils import insert_into_es
from uuid import uuid4
import json
import requests
from constants import POST_REVIEW_URL
import os

def insert_data_in_db(scraped_data, campaign_id, product_url):
    es_bulk_data = []
    # print(scraped_data)
    for each_rec in scraped_data:
        each_rec['campaign_id'] = campaign_id
        each_rec['product_url'] = product_url
        each_rec['review_date'] = str(each_rec['review_date'])
        es_data = {
            # '_id': str(uuid4()),
            '_index': 'user_reviews',
            '_source': each_rec
        }
        es_bulk_data.append(es_data)
    print()
    print(json.dumps(es_bulk_data))
    print()
    # insert_into_es(es_bulk_data)
    if int(os.environ.get('INSERT_DB', 0)) == 1:
        send_to_db(es_bulk_data)

def send_to_db(es_bulk_data):
    payload = json.dumps(es_bulk_data)
    headers = {
    'Content-Type': 'application/json',
    'Cookie': 'session=c2336f68-786d-4ab6-936f-47ae5dcd84ad; session=c2336f68-786d-4ab6-936f-47ae5dcd84ad'
    }
    url = POST_REVIEW_URL
    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)