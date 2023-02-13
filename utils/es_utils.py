from utils.connection_utils import getElasticSearchClient
import json
from elasticsearch import helpers
import traceback


def insert_into_es(data):
    try:
        es = getElasticSearchClient()
        print()
        print()
        print()
        print(data)
        print()
        print()
        print()
        if not es.indices.exists(index='user_reviews'):
            es.indices.create('user_reviews', ignore=400)
        response = helpers.bulk(es, actions=data)
        print("response-",response)
    except Exception:
        traceback.print_exc()        
