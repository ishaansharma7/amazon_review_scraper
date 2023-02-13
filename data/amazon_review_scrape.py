import requests
from bs4 import BeautifulSoup
from utils.amazon_utils import (get_date_time_object, get_review_url, date_from_date_span_text,
get_review_title, get_review_body, get_review_score, get_variant_info, get_start_date, get_end_date)
from utils.review_db_utils import insert_data_in_db
import time
import traceback


def scrape_procedure(product_url=None, start_date=None, end_date=None, campaign_id=None):
    """
    Start the scraping procedure with vital data like product url,
    start & end date.
    Adds meta data to scraped data before inserting into db
    """
    start_date = get_start_date()
    end_date = get_end_date(end_date)
    scraped_data = get_review_data(product_url ,start_date, end_date)
    # insert_data_in_db(scraped_data, campaign_id)


def get_review_data(product_url=None, start_date=None, end_date=None):
    """
    contains the logic scraping data from each page also remaining
    between the date constraint.
    This function collects that from each page and append that to
    scraped data list. 
    """
    page_number = 0
    scraped_data = []
    current_date = start_date
    while page_number < 40 and current_date and current_date >= end_date:
        page_number += 1
        review_url = get_review_url(product_url, page_number)
        print(review_url)
        print()
        local_data, current_date = get_review_cleaned_data(review_url, start_date, end_date) # this will only return data if it lies b/w the range, and also return date of last review for loop break condition
        scraped_data.extend(local_data)
        print('current_date:', current_date, ', page_number:', page_number)
        print()
        print('************************')
    return scraped_data


def get_review_cleaned_data(review_url, start_date, end_date, retry=6):
    if retry < 1:
        print('retry over ----')
        return [], None
    try:
        reviewer_name = None
        review_text = None
        review_score = None
        review_date = None
        verified_purchase = None
        current_date = None
        data_list = []
        page = requests.get(review_url)
        soup = BeautifulSoup(page.content, "html.parser")
        review_div = soup.find("div", {"id": "cm_cr-review_list"})
        review_div_list = review_div.find_all("div", {"class": "a-section review aok-relative"})
        for each in review_div_list:
            date_span = each.find("span", {"data-hook":"review-date"})
            name_span = each.find("span", {"class":"a-profile-name"})
            current_date = date_from_date_span_text(date_span.text)
            if current_date >= start_date or current_date <= end_date:
                continue
            # do data extraction here
            reviewer_name = name_span.text
            review_title = get_review_title(each)
            review_text = get_review_body(each)
            review_score = get_review_score(each)
            variant_info = get_variant_info(each)
            verified_purchase = True if each.find("span", {"data-hook":"avp-badge"}) else False
            review_date = current_date
            collected_data = {
                'reviewer_name': reviewer_name,
                'review_title': review_title,
                'review_text': review_text,
                'review_score': review_score,
                'verified_purchase': verified_purchase,
                'review_date': review_date,
                'review_score': review_score,
                'variant_info': variant_info,
            }
            data_list.append(collected_data)
            print('reviewer:', name_span.text)
            print('title:', review_title)
            print('body:', review_text)
            print('date:', current_date)
            print('verified purchase:', verified_purchase)
            print('review_score:', str(review_score) + '%')
            print('variant_info:', variant_info)
            print()

        return data_list, current_date
    except Exception:
        traceback.print_exc()
        return get_review_cleaned_data(review_url, start_date, end_date, retry-1)

    
    # for images  a-section a-spacing-medium review-image-container
    # for videos  vse-airy-container vse-player-container
    # username genome-widget



# from data.amazon_review_scrape import scrape_procedure
# '2022-12-31', '2022-12-01'