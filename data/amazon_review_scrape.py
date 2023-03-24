import requests
from bs4 import BeautifulSoup
from utils.amazon_utils import (get_date_time_object, get_review_url, date_from_date_span_text,
get_review_title, get_review_body, get_review_score, get_variant_info, get_start_date, get_end_date, get_product_code)
from utils.review_db_utils import insert_data_in_db
import time
import traceback
from constants import PAGE_LIMIT
import random



def scrape_procedure(product_url=None, start_date=None, end_date=None, campaign_id=None):
    """
    Start the scraping procedure with vital data like product url,
    campaign_id.
    Adds meta data to scraped data before inserting into db
    """
    # start_date is latest date, end_date is oldest date
    start_date = get_date_time_object(start_date) if start_date else get_start_date()
    end_date = get_date_time_object(end_date) if end_date else get_end_date(end_date, campaign_id)
    print(start_date, type(start_date))
    print(end_date, type(end_date))
    scraped_data = get_review_data(product_url ,start_date, end_date)
    insert_data_in_db(scraped_data, campaign_id, product_url)


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
    while page_number < PAGE_LIMIT and current_date and current_date >= end_date:
        page_number += 1
        review_url = get_review_url(product_url, page_number)
        if not review_url: break
        print(review_url)
        print()
        local_data, current_date = get_review_cleaned_data(review_url, start_date, end_date) # this will only return data if it lies b/w the range, and also return date of last review for loop break condition
        scraped_data.extend(local_data)
        print('current_date:', current_date, ', page_number:', page_number)
        print()
        print('************************')
        if not current_date:
            break
        time.sleep(random.randint(3,7))
        
    return scraped_data


def get_review_cleaned_data(review_url, start_date, end_date, retry=15):
    if retry < 1:
        print('retry over ----')
        return [], None
    try:
        reviewer_name = None
        review_text = None
        review_score = None
        review_date = None
        verified_purchase = None
        review_title = None
        current_date = None
        data_list = []
        # page = requests.get(review_url)
        # soup = BeautifulSoup(page.content, "html.parser")
        proxies = {'https': '27.239.65.23:8085'}
        headers = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/90.0.4430.212 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
        print('url:-', review_url)
        source = requests.get(url=review_url)
        # source = requests.get('http://localhost:8050/render.html', params={'url': review_url, 'wait':2})
        soup = BeautifulSoup(source.text, 'lxml')

        # time.sleep(3)
        # print(soup.text)
        # time.sleep(30)
        review_div = soup.find("div", {"id": "cm_cr-review_list"})
        review_div_list = review_div.find_all("div", {"class": "a-section review aok-relative"})
        for each in review_div_list:
            date_span = each.find("span", {"data-hook":"review-date"})
            name_span = each.find("span", {"class":"a-profile-name"})
            current_date = date_from_date_span_text(date_span.text)
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
            print('reviewer:', name_span.text)
            print('title:', review_title)
            print('body:', review_text)
            print('date:', current_date)
            print('verified purchase:', verified_purchase)
            print('review_score:', str(review_score) + '%')
            print('variant_info:', variant_info)
            print()
            if current_date > start_date or current_date < end_date:
                continue
            data_list.append(collected_data)

        return data_list, current_date
    except Exception:
        traceback.print_exc()
        if soup:
            msg = soup.text
            if msg:
                msg = msg.replace('\n', ' ').strip()
                print(msg)
                del source
                del soup
        print('exception in scraping------')
        refresh(review_url)
        time.sleep(random.randint(3,7))
        return get_review_cleaned_data(review_url, start_date, end_date, retry-1)

def refresh(review_url):
    # product_code = get_product_code(review_url)
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'}
    # product_page = 'https://www.amazon.in/dp/' + product_code
    product_page = 'https://www.amazon.in/'
    source = requests.get(product_page, headers=headers)
    print('refresh ran ')
