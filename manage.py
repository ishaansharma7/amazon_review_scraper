from datetime import datetime, timedelta
from flask import current_app
from main import create_app
import os
application = create_app()
import time
from scripts.test_script import hello_world
from data.amazon_review_scrape import scrape_procedure


@application.cli.command('test_cmd')
def func_test_cmd():
   hello_world()

@application.cli.command('scrape_amazon')
def scrape_amazon():
   product_url = 'https://www.amazon.in/ASUS-15-6-inch-GeForce-Windows-FA506IHRZ-HN111W/dp/B0B5DZTNZQ?ref_=Oct_DLandingS_D_66dc9eef_60&th=1'
   start_date = '2023-02-08'
   end_date = '2022-12-10'
   scrape_procedure(product_url, start_date, end_date)