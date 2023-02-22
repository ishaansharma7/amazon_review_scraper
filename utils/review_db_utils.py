from utils.es_utils import insert_into_es
from uuid import uuid4
import json

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
