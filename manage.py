from datetime import datetime, timedelta
from flask import current_app
from main import create_app
application = create_app()
import os
# import time
from time import time
from scripts.amazon_scrape_job import hello_world
from data.amazon_review_scrape import scrape_procedure
from utils.es_utils import insert_into_es
from data.image_extract import read_image
import click
import csv
from campaign_det import cam_details
from cam_ss import ss_details
import requests
import pandas as pd
import json


@application.cli.command('test_cmd')
def func_test_cmd():
   hello_world()


@application.cli.command('insert_data')
def insert_data():
   insert_into_es()


@application.cli.command('scrape_amazon')
def scrape_amazon():
   product_url = 'https://www.amazon.in/dp/B0BQRM1NMG/ref=sr_1_2?keywords=dermatouch%2Bsunscreen%2Bspf%2B50&qid=1676459442&sprefix=dermat%2Caps%2C362&sr=8-2&th=1'
   # end_date = '2022-12-10'
   scrape_procedure(product_url=product_url, campaign_id=1004)


@application.cli.command('single_test')
@click.option('--loc')
def single_test(loc):
   read_image(filename=loc, campaign_id=1004)

   
@application.cli.command('single_test_url')
def single_test():
   img_link = "https://firebasestorage.googleapis.com/v0/b/api-project-3577377239.appspot.com/o/user%2F7c1984ae9ab84e9492516635bc071afc%2Fmedia%2Fdocument%2Fimage%3A1000003284_20221028_095221?alt=media&token=2da258b9-77e8-445a-9b51-33dd5b6739ea"
   read_image(img_link=img_link, campaign_id=12533)


@application.cli.command('scrape_campaigns')
def scrape_campaigns():
   total_cam = len(cam_details)
   for idx, cam in enumerate(cam_details, 1):
      print('**********', cam['campaign_id'], f',current: {idx}/{total_cam}','**********')
      r = requests.get(cam['buy_now_link'])
      product_url = r.url
      print('url:', product_url)
      end_date = '2022-11-15'
      start_date = '2023-01-05'
      # end_date = '2023-02-01'
      # start_date = '2023-02-20'
      scrape_procedure(product_url=product_url, campaign_id=cam['campaign_id'], start_date=start_date, end_date=end_date)
      print('******************************')


@application.cli.command('campaign_images')
def campaign_images():
   print('start time-----',datetime.now())
   start_epoch = time()
   images_data = []
   len_ss = len(ss_details)
   scraped_cams = [rec_cam['campaign_id'] for rec_cam in cam_details]
   sub_status = {0:'draft', 1:'pending', 2:'rejected', 3:'approved'}
   for idx, rec in enumerate(ss_details, 1):
      # if idx == 11:
      #    break
      print('**********', rec['campaign_id'], f',current: {idx}/{len_ss}','**********')
      if rec['campaign_id'] not in scraped_cams:
         print('not from scraped campaign')
         continue

      res_dict = read_image(img_link=rec['url'], campaign_id=rec['campaign_id'], product_url=rec['buy_now_link'], user_id=rec['user_id'])
      images_data.append(res_dict)

      submi_status = sub_status[rec.get('proof_status', 3)]
      matched_rec = res_dict['matched_rec']
      res_dict.pop('matched_rec')
      row = {
         'image_json_post_ocr': json.dumps(res_dict),
         'review_scrapper_json': json.dumps(matched_rec) if res_dict['found_rec'] else 'null',
         'product_url': res_dict['product_url'],
         'date_in_ss': res_dict['review_date'],
         'ocr_success': res_dict['ocr_success'],
         'submi_status': submi_status,
         'ocr_status': 'approved' if res_dict['valid_review'] else 'rejected',
         'campaign_id': res_dict['campaign_id'],
         'user_id': res_dict['user_id'],
         'image_url': res_dict['img_link'],
         'reason': res_dict['reason'],
      }
      file_exists = os.path.isfile('ocr_output.csv')

      # Create a pandas DataFrame from the list of dictionaries
      df = pd.DataFrame([row])

      # Append the DataFrame to the CSV file if it already exists, otherwise create a new file
      if file_exists:
         df.to_csv('ocr_output.csv', mode='a', header=False, index=False)
      else:
         df.to_csv('ocr_output.csv', index=False)
      
      print('******************************')
   print('end time-----',datetime.now())
   end_seconds = time() - start_epoch
   print('total duration-----', timedelta(seconds=end_seconds))
   print('\n \n \n')