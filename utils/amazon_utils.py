import re
from dateutil.parser import parse


def get_review_url(product_url, page_number=1):
    """
    Gets product url and returns the url of review page with most recent sorted
    """
    match = re.search(r'\b[A-Z0-9]{10}\b', product_url)
    start_idx = match.start()
    product_code = product_url[start_idx:start_idx+10]
    review_url = 'https://www.amazon.in/product-reviews/' +product_code+ "?ref=cm_cr_arp_d_viewopt_srt%3FsortBy%3Drecent&pageNumber="+ str(page_number) + "&sortBy=recent"
    return review_url

def get_date_time_object(date_str):
    return parse(date_str)


def date_from_date_span_text(date_str):
    try:
        date_str = date_str.split(' on ')[-1]
        return parse(date_str)
    except Exception:
        print('review date extraction failed ----')
    return None


def get_review_title(review_html):
    try:
        review_title = review_html.find("a", {"data-hook":"review-title"})
        review_title = review_title.text.strip()
        review_title = review_title.replace('\n', '')
        return review_title
    except Exception:
        print('review date extraction failed ----')
    return None

def get_review_body(review_html):
    try:
        review_body = review_html.find("span", {"data-hook":"review-body"})
        review_body = review_body.text.strip()
        review_body = review_body.replace('\n', '')
        return review_body
    except Exception:
        print('review body extraction failed ----')
    return None

def get_review_score(review_html):
    try:
        score_html = review_html.find("i", {"data-hook":"review-star-rating"})
        score_text = score_html.text.strip()
        score_text = score_text.replace('\n', '')
        score_text = score_text.split(' out')[0]
        score_perc = float(score_text)*20
        return score_perc
    except Exception:
        print('review score extraction failed ----')
    return None

def get_variant_info(review_html):
    try:
        variant_html = review_html.find("a", {"data-hook":"format-strip"})
        variant_text = variant_html.text.strip()
        variant_text = variant_text.replace('\n', '')
        return variant_text
    except Exception:
        print('review score extraction failed ----')
    return None