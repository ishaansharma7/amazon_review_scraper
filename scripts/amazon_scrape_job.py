from data.amazon_review_scrape import scrape_procedure
import requests

def amazon_scrape_job():
    cam_details = live_campaigns_list()
    tot_cam = len(cam_details)
    for idx, cam in enumerate(cam_details, 1):
        print(f'************ Currently: {idx}/{tot_cam} ************')
        print('campaign_id:---', cam['campaign_id'])
        print('product_link:---', cam['buy_now_link'])
        scrape_procedure(product_url=cam['buy_now_link'], campaign_id=cam['campaign_id'])
        print('********************************')


def live_campaigns_list():
    """
    return list of live campaigns for the previous day
    """
    cam_details = [
        {"campaign_id":12533,"buy_now_link":"https://amzn.to/3rExEid"},
        # {"campaign_id":14356,"buy_now_link":"https://amzn.to/3uG60mf"},
        # {"campaign_id":14565,"buy_now_link":"https://amzn.to/3FxiQcG"}
    ]
    for cam in cam_details:
        r = requests.get(cam['buy_now_link'])
        cam['buy_now_link'] = r.url
    return cam_details


def hello_world():
    print ("hello world")