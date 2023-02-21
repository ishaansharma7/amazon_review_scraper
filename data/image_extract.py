from utils.ocr_utils import prepare_image, clean_extracted_text, extract_data, match_from_db
import pytesseract
import traceback
import json


def read_image(filename=None, img_link=None, product_url='', campaign_id=1000):
    
    # extracted data
    ex_da = {
        'product_url': product_url,
        'reviewer_name': None,
        'review_title': None,
        'review_text': None,
        'verified_purchase': None,
        'thanks_message': None,
        'edit_button': None,
        'delete_button': None,
        'valid_review': False,
        'found_rec': False,
        'matched_rec': None,
        'img_link': img_link,
        'campaign_id': campaign_id,
    }
    try:
        image, success = prepare_image(filename, img_link)
        if not success:   return ex_da

        data_eng = pytesseract.image_to_string(image, lang='eng')
        data_eng = clean_extracted_text(data_eng)

        extract_data(data_eng, ex_da)
        match_from_db(ex_da)

        print('\n\n\n\n')
        print(json.dumps(ex_da, indent=5))
        print('###############################')

    except Exception:
        traceback.print_exc()
    return ex_da