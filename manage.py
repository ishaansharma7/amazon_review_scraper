from datetime import datetime, timedelta
from flask import current_app
from main import create_app
import os
application = create_app()
import time
from scripts.test_script import hello_world
from data.amazon_review_scrape import scrape_procedure
from utils.es_utils import insert_into_es


@application.cli.command('test_cmd')
def func_test_cmd():
   hello_world()

@application.cli.command('scrape_amazon')
def scrape_amazon():
   product_url = 'https://www.amazon.in/OnePlus-Nord-Lite-128GB-Storage/dp/B09WQYFLRX/ref=pd_rhf_d_eebr_s_pd_crcd_sccl_2_2/259-4329364-8343312?pd_rd_w=CI01Q&content-id=amzn1.sym.dcf9b861-ea71-4cd9-870f-f1d20747f687&pf_rd_p=dcf9b861-ea71-4cd9-870f-f1d20747f687&pf_rd_r=T5KMM5K4ZH3V3059BTAT&pd_rd_wg=3kuhg&pd_rd_r=4255ef40-0c69-4ae2-8c2c-9ca61fe9c12c&pd_rd_i=B09WQYFLRX&psc=1'
   # end_date = '2022-12-10'
   scrape_procedure(product_url=product_url, campaign_id=1002)


@application.cli.command('insert_data')
def insert_data():
   insert_into_es()