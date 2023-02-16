from datetime import datetime, timedelta
from flask import current_app
from main import create_app
import os
application = create_app()
import time
from scripts.test_script import hello_world
from data.amazon_review_scrape import scrape_procedure
from utils.es_utils import insert_into_es
from utils.image_extract import read_image
import click


@application.cli.command('test_cmd')
def func_test_cmd():
   hello_world()

@application.cli.command('scrape_amazon')
def scrape_amazon():
   product_url = 'https://www.amazon.in/dp/B0BQRM1NMG/ref=sr_1_2?keywords=dermatouch%2Bsunscreen%2Bspf%2B50&qid=1676459442&sprefix=dermat%2Caps%2C362&sr=8-2&th=1'
   # end_date = '2022-12-10'
   scrape_procedure(product_url=product_url, campaign_id=1004)


@application.cli.command('insert_data')
def insert_data():
   insert_into_es()


@application.cli.command('image_test')
@click.option('--loc')
def image_test(loc):
   read_image(loc)