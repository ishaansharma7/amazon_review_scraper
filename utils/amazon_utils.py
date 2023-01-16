import re
from dateutil.parser import parse


def get_review_url(product_url, page_number=1):
    match = re.search(r'\b[A-Z0-9]{10}\b', product_url)
    start_idx = match.start()
    product_code = product_url[start_idx:start_idx+10]
    review_url = 'https://www.amazon.in/product-reviews/' +product_code+ "?ref=cm_cr_arp_d_viewopt_srt%3FsortBy%3Drecent&pageNumber="+ str(page_number) + "&sortBy=recent"
    return review_url

def get_date_time_object(date_str):
    return parse(date_str)