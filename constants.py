import os
from flask import current_app

POST_REVIEW_URL= os.environ['API_BASE_URL'] + '/v1/review-campaign-data/reviews/'
# POST_REVIEW_URL= current_app.config['API_BASE_URL'] + '/v1/review-campaign-data/reviews/'