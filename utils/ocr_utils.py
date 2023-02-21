import cv2
import traceback
import json
import requests
import io
from PIL import Image
from utils.connection_utils import getElasticSearchClient

def prepare_image(filename, img_link):
    """
    get image either locally or by image link,
    also returns B&W image and a boolean success
    """
    try:
        if not img_link:
            image = cv2.imread(filename)
            gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            (thresh, bw_img) = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY)
            image = bw_img
        else:
            response = requests.get(img_link)
            if response.status_code != 200:
                print('response.status_code', response.status_code)
                print('image download failed ---')
                return None, False
            image = Image.open(io.BytesIO(response.content))
            bw_img = image.convert('L')
            image = bw_img
        return image, True
    except Exception:
        traceback.print_exc()
    return None, False


def extract_data(data_eng, ex_da):

    if not initial_keyword_check(data_eng):
        print('anchor keyword not found')
        return False
    
    data_eng = data_eng.strip()
    line_list = data_eng.split('\n')
    
    # print ocr text with index
    for index, line in enumerate(line_list):
        print(f'[{index}]:',line)

    idx = find_target_reviewed_in_india(line_list)

    # checks if screenshot is not cropped ie contains title
    if not idx and idx-3<0:
        print('out of index ----')
        return

    in_india_idx = idx  # Reviewed in India
    if 'Verified Purchase' not in line_list[in_india_idx-3]:       # means title is of 1 line
        ex_da['reviewer_name'] = clean_name(line_list[in_india_idx-3])
        ex_da['review_title'] = clean_title1(in_india_idx, line_list)
    else:   # means title is of 2 line
        ex_da['reviewer_name'] = clean_name(line_list[in_india_idx-4])
        ex_da['review_title'] = clean_title2(in_india_idx, line_list)

    #### trying to catch review text block ####
    idx = find_index_using_keyword(line_list, 'Thank you for your review')
    thank_idx = idx

    if variant_info_available(ex_da['campaign_id']):    # skip the variant info line and get review body
        review_text = clean_review_text(in_india_idx+1, thank_idx, line_list)
    else:
        review_text = clean_review_text(in_india_idx, thank_idx, line_list)
    #### trying to catch review text block ####

    ex_da['review_text'] = review_text

    ex_da['verified_purchase'] = True if 'Verified Purchase' in data_eng else False
    ex_da['thanks_message'] = True if 'Thank you for your review' in data_eng else False
    ex_da['edit_button'] = True if 'Edit Delete' in data_eng else False
    ex_da['delete_button'] = True if 'Edit Delete' in data_eng else False
    ex_da['valid_review'] = True

    

def match_from_db(ex_da):
    query = {
    "query": {
        "bool": {
        "must": [
            {
            "term": {
                "campaign_id": ex_da['campaign_id']
            }
            },
            {
            "query_string": {
                "query": ex_da['review_title'],
                "default_field": "review_title"
            }
            },
            {
            "query_string": {
                "query": ex_da['review_text'],
                "default_field": "review_text"
            } 
            }
        ]
        }
    }
    }
    es = getElasticSearchClient()
    print()
    print(json.dumps(query, indent=2))
    es_res = es.search(index='user_reviews', body=query)
    print('max_score:',  es_res['hits'].get('max_score'))
    if not es_res['hits']['max_score'] or es_res['hits'].get('max_score', 1) < 90:
        return
    ex_da['found_rec'] = True
    ex_da['matched_rec'] = es_res['hits']['hits'][0]['_source']


def initial_keyword_check(data_eng):
    """
    check basic keywords are present for authentic review
    """
    if 'Reviewed in India' in data_eng and 'Thank you for your review' in data_eng and 'Verified Purchase' in data_eng:
        return True
    return False

def find_index_using_keyword(line_list, keyword):
    """
    returns the index of line in which keyword is present
    """
    idx = 0
    for line in line_list:
        if keyword in line:
            return idx
        idx += 1
    return None


def find_target_reviewed_in_india(line_list):
    """
    this will find `Reviewed in India` just above the `Thank you for your review` line,
    basically finds the user own review instead of others
    """
    try:
        idx = 0
        for index, line in enumerate(line_list):
            if 'Reviewed in India' in line:
                idx = index
            if 'Thank you for your review' in line:
                return idx
    except Exception:
        traceback.print_exc()
    return None

def clean_extracted_text(data_eng):
    data_eng = data_eng.replace('\n\n', '\n')
    cleaned_data = ''
    for char in data_eng:
        if char.isalnum() or char in ['.', ',', '-', ' ', '\n']:
            cleaned_data += char
    return cleaned_data

def clean_name(rv_name):
    try:
        rv_name = rv_name.strip()
        return rv_name
    except Exception:
        traceback.print_exc()
    return None

def clean_title1(in_india_idx, line_list):
    """
    returns the title that is present just 1 line above `Reviewed in India`
    """
    try:
        title_idx = in_india_idx-1
        return line_list[title_idx]
    except Exception:
        traceback.print_exc()
    return None


def clean_title2(in_india_idx, line_list):
    """
    returns the combined title that is present
    2 and 1 line above `Reviewed in India`
    """ 
    try:
        title_idx = in_india_idx-2
        return ' '.join(line_list[title_idx: in_india_idx])
    except Exception:
        traceback.print_exc()
    return None

def clean_review_text(in_india_idx, thank_idx, line_list):
    """
    catch the review text and combine lines in single paragraph
    """
    try:
        review_text_list = line_list[in_india_idx+1: thank_idx]
        review_text = ' '.join(review_text_list)
        return review_text
    except Exception:
        traceback.print_exc()
    return None


def variant_info_available(campaign_id):
    """
    return True if variant info is available for product
    """
    try:
        es = getElasticSearchClient()
        query = {
            "query": {
                "bool": {
                "must": [
                    {
                    "term": {
                        "campaign_id": campaign_id
                    }
                    }
                ]
                }
            }
            , "size": 1
        }
        es_res = es.search(index='user_reviews', body=query)
        if len(es_res['hits']['hits']) > 0:
            variant_info = es_res['hits']['hits'][0]['_source']['variant_info']
            print('variant_info:', variant_info)
            if variant_info != '' and variant_info != None:
                return True
    except Exception:
        traceback.print_exc()
    return False