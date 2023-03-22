import os
from flask import current_app

PAGE_LIMIT = int(os.environ.get('PAGE_LIMIT', 50))
POST_REVIEW_URL= os.environ['API_BASE_URL'] + '/v1/review-campaign-data/reviews/'
LAST_DATE_URL= os.environ['API_BASE_URL'] + '/v1/review-campaign-data/last-date/'
# POST_REVIEW_URL= current_app.config['API_BASE_URL'] + '/v1/review-campaign-data/reviews/'