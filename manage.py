from datetime import datetime, timedelta
from flask import current_app
from main import create_app
import os
application = create_app()
import time
from scripts.test_script import hello_world
from data.amazon_review_scrape import scrape_procedure
from utils.es_utils import insert_into_es
from data.image_extract import read_image
import click
import csv


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
def image_test():
   images_data = []
   cols = [
      'reviewer_name',
      'review_title',
      'review_text',
      'verified_purchase',
      'thanks_message',
      'edit_button',
      'delete_button',
      'valid_review',
      'img_link',
   ]
   with open('images_link.csv') as f:
      reader = csv.reader(f)
      for idx, row in enumerate(reader):
         image_url, filename = row
         print('current:-', idx)
         images_data.append(read_image(img_link=image_url))
   

   with open('ocr_output.csv', 'w', newline='') as f:
      writer = csv.DictWriter(f, fieldnames=cols)
      
      # Write the column headers to the first row
      writer.writeheader()
      
      # Write each dictionary as a row in the CSV file
      for d in images_data:
         writer.writerow(d)

@application.cli.command('single_test')
@click.option('--loc')
def single_test(loc):
   read_image(filename=loc, campaign_id=1004)