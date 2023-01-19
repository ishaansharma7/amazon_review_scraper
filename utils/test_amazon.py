import requests
from bs4 import BeautifulSoup


URL = "https://www.amazon.in/LOreal-Paris-Extraordinary-Serum-Women/product-reviews/B08FW1GJ4F/ref=cm_cr_arp_d_viewopt_srt?sortBy=recent&pageNumber=1"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
review_div = soup.find("div", {"id": "cm_cr-review_list"})
review_div_list = review_div.find_all("div", {"class": "a-section review aok-relative"})
for each in review_div_list:
    date_span = each.find("span", {"data-hook":"review-date"})
    print(each.text)
    print()