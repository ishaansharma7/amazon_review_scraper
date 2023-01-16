import requests
from bs4 import BeautifulSoup
from utils.amazon_utils import get_date_time_object, get_review_url
from utils.review_db_utils import insert_data_in_db


def scrape_procedure(product_url=None, start_date=None, end_date=None):
    start_date = get_date_time_object(start_date)
    end_date = get_date_time_object(end_date)
    scraped_data = get_review_data(product_url ,start_date, end_date)
    insert_data_in_db(scraped_data)


def get_review_data(product_url=None, start_date=None, end_date=None):
    page_number = 0
    scraped_data = []
    current_date = start_date
    while page_number < 5 and current_date >= end_date:
        page_number += 1
        review_url = get_review_url(product_url, page_number)
        local_data, current_date = get_review_cleaned_data(review_url, start_date, end_date) # this will only return data if it lies b/w the range, and also return date of last review for loop break condition
        scraped_data.extend(local_data)
    return scraped_data


def get_review_cleaned_data(review_url, start_date, end_date):
    page = requests.get(review_url)
    soup = BeautifulSoup(page.content, "html.parser")
    review_div = soup.find("div", {"id": "cm_cr-review_list"})
    review_div_list = review_div.find_all("div", {"class": "a-section review aok-relative"})
    for each in review_div_list:
        date_span = each.find("span", {"data-hook":"review-date"})
        print(date_span.prettify())