from utils.ocr_utils import prepare_image, clean_extracted_text, extract_data, match_from_db
import pytesseract
import traceback
import json
import time


def read_image(filename=None, img_link=None, user_id=None,campaign_id=1000, real_time=False, platform=''):
    
    # extracted data
    ex_da = {
        'reviewer_name': None,
        'review_title': None,
        'review_text': None,
        'verified_purchase': None,
        'thanks_message': None,
        'edit_button': None,
        'delete_button': None,
        'valid_review': False,
        'ocr_success': False,
        'found_rec': False,
        'matched_rec': None,
        'img_link': img_link,
        'campaign_id': campaign_id,
        'review_date': None,
        'user_id': user_id,
        'platform': platform,
        'reason':''
    }
    try:
        image, success = prepare_image(filename, img_link)
        if not success:   return ex_da

        data_eng = pytesseract.image_to_string(image, lang='eng')
        data_eng = clean_extracted_text(data_eng)

        extract_data(data_eng, ex_da)

        if ex_da['review_title'] != None and ex_da['review_text'] != None and not real_time:
            print('db match ---')
            match_from_db(ex_da)

        ex_da['valid_review'] = True if ex_da['ocr_success'] and ex_da['found_rec'] else False
        if ex_da['valid_review']:
            ex_da['reason'] = {'code': '6', 'msg': 'Authentic amazon review'}
        print('\n\n\n\n')
        print(json.dumps(ex_da, indent=5))
        print('###############################')

    except Exception:
        traceback.print_exc()
    return ex_da