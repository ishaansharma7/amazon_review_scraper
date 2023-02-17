import cv2
import pytesseract
import traceback
import json
import requests
import io
from PIL import Image
import time

def read_image(filename=None, img_link=None):
    ex_da = {                   # extracted data
        'reviewer_name': None,
        'review_title': None,
        'review_text': None,
        'verified_purchase': None,
        'thanks_message': None,
        'edit_button': None,
        'delete_button': None,
        'valid_review': False,
        'img_link': img_link,
    }
    if not img_link:
        image = cv2.imread(filename)
    else:
        response = requests.get(img_link)
        if response.status_code != 200:
            print('response.status_code', response.status_code)
            print('image download failed ---')
            return ex_da
        image = Image.open(io.BytesIO(response.content))

    data_eng = pytesseract.image_to_string(image, lang='eng')
    # print(data_eng)
    data_eng = clean_extracted_text(data_eng)
    verify_extracted_data(data_eng, ex_da)
    # time.sleep(0.5)
    print('###############################')
    return ex_da


def verify_extracted_data(data_eng, ex_da):
    if not initial_keyword_check(data_eng):
        print('anchor keyword not found')
        return False
    
    data_eng = data_eng.strip()

    line_list = data_eng.split('\n')
    for index, line in enumerate(line_list):
        print(f'[{index}]:',line)
    idx = find_target_reviewed_in_india(line_list)

    # print()
    # print('idx', idx)
    if not idx and idx-3<0:
        # do a direct search in db
        print('anchor keyword not found')
        return
    in_india_idx = idx  # Reviewed in India
    if 'Verified Purchase' not in line_list[in_india_idx-3]:       # means title is of 1 line
        # print('reviewer_name:', clean_name(line_list[in_india_idx-3]))
        # print('review_title:', clean_title1(in_india_idx, line_list))
        ex_da['reviewer_name'] = clean_name(line_list[in_india_idx-3])
        ex_da['review_title'] = clean_title1(in_india_idx, line_list)
    else:   # means title is of 2 line
        # print('reviewer_name:', clean_name(line_list[in_india_idx-4]))
        # print('review_title:', clean_title2(in_india_idx, line_list))
        ex_da['reviewer_name'] = clean_name(line_list[in_india_idx-4])
        ex_da['review_title'] = clean_title2(in_india_idx, line_list)
    # return
    ### trying to catch review text block ###
    idx = find_index_using_keyword(line_list, 'Thank you for your review')
    thank_idx = idx
    review_text = clean_review_text(in_india_idx, thank_idx, line_list)
    ex_da['review_text'] = review_text

    ex_da['verified_purchase'] = True if 'Verified Purchase' in data_eng else False
    ex_da['thanks_message'] = True if 'Thank you for your review' in data_eng else False
    ex_da['edit_button'] = True if 'Edit Delete' in data_eng else False
    ex_da['delete_button'] = True if 'Edit Delete' in data_eng else False
    ex_da['valid_review'] = True
    print()
    print()
    print()
    print(json.dumps(ex_da, indent=5))

    

def initial_keyword_check(data_eng):
    if 'Reviewed in India' in data_eng and 'Thank you for your review' in data_eng:
        return True
    return False


def extract_info(data_eng):
    ### First check image of type `Thank you for your review`
    pass

def find_index_using_keyword(line_list, keyword):
    idx = 0
    for line in line_list:
        if keyword in line:
            return idx
        idx += 1
    return None

def find_target_reviewed_in_india(line_list):
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
        name_list = rv_name.split()
        if len(name_list) <=1:
            return name_list[0]
        return ' '.join(name_list[1:])
    except Exception:
        traceback.print_exc()
    return None

def clean_title1(in_india_idx, line_list):
    try:
        title_idx = in_india_idx-1
        return line_list[title_idx]
    except Exception:
        traceback.print_exc()
    return None


def clean_title2(in_india_idx, line_list):
    try:
        title_idx = in_india_idx-2
        return ' '.join(line_list[title_idx: in_india_idx])
    except Exception:
        traceback.print_exc()
    return None

def clean_review_text(in_india_idx, thank_idx, line_list):
    try:
        review_text_list = line_list[in_india_idx+1: thank_idx]
        review_text = ' '.join(review_text_list)
        return review_text
    except Exception:
        traceback.print_exc()
    return None
