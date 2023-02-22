from utils.connection_utils import getElasticSearchClient
import json
from elasticsearch import helpers
import traceback
from datetime import datetime, timedelta
from dateutil.parser import parse


def insert_into_es(data):
    try:
        es = getElasticSearchClient()
        for each in data:
            print(each)
            each['_source']['review_date'] = parse(each['_source']['review_date'])
        if not es.indices.exists(index='user_reviews'):
            es.indices.create('user_reviews', ignore=400)
        response = helpers.bulk(es, actions=data)
        print("response-",response)
    except Exception:
        traceback.print_exc()        

def get_last_date(campaign_id=None):
    try:
        query = {
            "query": {
                    "bool": {
                    "must": [
                        {
                        "term": {
                            "campaign_id": campaign_id
                        }
                        }
                    ]
                    }
                },
            "sort": [
                    {
                    "review_date": {
                        "order": "desc"
                    }
                }
            ]
        }
        es = getElasticSearchClient()
        res = es.search(index='user_reviews', body=query)
        if len(res['hits']['hits']) > 0:
            rec = res['hits']['hits'][0]['_source']
            # print(rec['review_date'], type(rec['review_date']))
            return parse(rec['review_date']) + timedelta(days=1)
    except Exception:
        traceback.print_exc()
    return None