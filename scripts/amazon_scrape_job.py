from data.amazon_review_scrape import scrape_procedure
import requests
from constants import LIVE_CAM_URL
import os


def amazon_scrape_job():
    cam_details = live_campaigns_list()
    tot_cam = len(cam_details)
    for idx, cam in enumerate(cam_details, 1):
        print(f'************ Currently: {idx}/{tot_cam} ************')
        print('campaign_id:---', cam['campaign_id'])
        print('product_link:---', cam['buy_now_link'])
        if not cam['campaign_id'] or not cam['buy_now_link']:
            print('missing details---')
            continue
        r = requests.get(cam['buy_now_link'])
        product_url = r.url
        scrape_procedure(product_url=product_url, campaign_id=cam['campaign_id'])
        print('********************************')


def live_campaigns_list():
    """
    return list of live campaigns for the current day
    """
    url = LIVE_CAM_URL
    payload={}
    headers = {
    'id': os.environ.get('USER_ID'),
    'Cookie': 'session=c2336f68-786d-4ab6-936f-47ae5dcd84ad'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    cam_details = response.json()['data']['result']
    print(cam_details)
    return cam_details


def hello_world():
    print ("hello world")