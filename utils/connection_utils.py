from flask import current_app
from elasticsearch import Elasticsearch

def getElasticSearchClient():
    es = Elasticsearch(current_app.config['ES_URL'])
    return es