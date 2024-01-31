import re
import cloudscraper

from bs4 import BeautifulSoup
from fake_useragent import UserAgent

def cloudscraper_get_page(url):
    scraper = cloudscraper.create_scraper()
    req = scraper.get(url)
    print(f"getting {req.status_code} from {url}")
    resp = req.text
    return resp
        
def get_link_from_page(html)->list:
    soup = BeautifulSoup(html,"html.parser")
    book_urls = []
    items = soup.find_all("div","MuiGrid-root MuiGrid-item MuiGrid-grid-xs-6 MuiGrid-grid-sm-4 MuiGrid-grid-md-4 MuiGrid-grid-lg-3")
    for item in items:
        url = item.find("a")["href"]
        book_urls.append(url)
    return book_urls
        
def get_categories(html)->list:
    result = []
    soup = BeautifulSoup(html,"html.parser")
    all_categories = soup.find_all("h5","MuiTypography-root MuiTypography-h5")
    all_categories = [category.text for category in all_categories]
    for item in all_categories:
        i = item.split()
        join = "%20".join(i).lower()
        url_category = f"https://bookoutlet.com/browse/products/{join}"
        result.append(url_category)
    return result

def max_pages(html)->int:
    soup = BeautifulSoup(html,"html.parser")
    pages = soup.find("p","MuiTypography-root MuiTypography-body1 MuiTypography-alignCenter").text
    match = re.search(r"of (\d+)",pages)
    if match:
        result = match.group(1)
        return int(result)
    
def loop_all_link(base_url)->list:
    all_link = []
    html = cloudscraper_get_page(base_url)

    list_url_categories = get_categories(html)
    for category in list_url_categories:
        category_html = cloudscraper_get_page(category)
        pages = max_pages(category_html)
        for page in range(1,pages+1):
            url_pages = f"{category}?page={page}"
            all_link.append(url_pages)
    with open("all_link.txt","w") as f:
        f.writelines([link + '\n' for link in all_link])
    return all_link

def main()->list:
    book_urls = []
    base_url = "https://bookoutlet.com/categories"
    all_category_page = loop_all_link(base_url)
    for category_page in all_category_page:
        print(f"from {category_page}")
        html = cloudscraper_get_page(category_page)
        book_url = get_link_from_page(html)
        print(f"============ get {len(book_urls)} links =================")
        book_urls.extend(book_url)
    return book_urls

if __name__=="__main__":
    result = main()
    with open("final_links.txt","w") as f:
        f.writelines([link + "," for link in result])