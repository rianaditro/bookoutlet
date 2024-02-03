from scraping.scrap_all_book_links import get_categories,get_link_from_page
from scraping.product_details import send_requests,parse_js


def all_categories():
    base_url = "https://bookoutlet.com/categories"
    html = send_requests(base_url)
    categories = get_categories(html)
    return categories

def open_page(url):
    html = send_requests(url)
    book_link = get_link_from_page(html)
    return book_link



