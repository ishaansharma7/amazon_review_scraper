import json
import requests
from constants import POST_REVIEW_URL
import os
from datetime import datetime
import hashlib


def insert_data_in_db(scraped_data, campaign_id, product_url, platform):
    es_bulk_data = []
    scrape_date = str(datetime.now())
    for each_rec in scraped_data:
        each_rec['campaign_id'] = campaign_id
        each_rec['product_url'] = product_url
        each_rec['review_date'] = str(each_rec['review_date'])
        each_rec['scrape_date'] = scrape_date
        each_rec['platform'] = platform
        es_data = {
            '_index': 'user_reviews',
            '_id': create_hash(each_rec['reviewer_name'], each_rec['review_title'], str(campaign_id)),
            '_source': each_rec,
            "doc_as_upsert": True
        }
        es_bulk_data.append(es_data)

    if int(os.environ.get('INSERT_DB', 0)) == 1 and es_bulk_data:
        send_to_db(es_bulk_data)
        print('data sent to api for campaign: ', campaign_id)
    else:
        print('data not sent to api for campaign: ', campaign_id)


def send_to_db(es_bulk_data):
    payload = json.dumps(es_bulk_data)
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'session=c2336f68-786d-4ab6-936f-47ae5dcd84ad; session=c2336f68-786d-4ab6-936f-47ae5dcd84ad'
    }
    url = POST_REVIEW_URL
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


def create_hash(*args):
    full_str = ' '.join(args)
    hobj = hashlib.sha256(full_str.encode())
    return hobj.hexdigest()