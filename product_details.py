from bs4 import BeautifulSoup

import cloudscraper,json


def send_requests(url):
    scraper = cloudscraper.create_scraper()
    req = scraper.get(url)
    print(f"getting {req.status_code} from {url}")
    resp = req.text
    return resp

def parse_html(html):
    result = []
    soup = BeautifulSoup(html,"html.parser")
    additional_info = soup.find("div","MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12 MuiGrid-grid-md-4 MuiGrid-grid-lg-6")
    p_tag = additional_info.find_all("p","MuiTypography-root MuiTypography-body1")
    for p in p_tag:
        result.append(p.text)
    return result

def parse_js(html):
    soup = BeautifulSoup(html,"html.parser")
    script_tag = soup.find("script",{"id":"__NEXT_DATA__"}).text.strip()
    json_loaded = json.loads(script_tag)["props"]["pageProps"]["details"]
    price = json_loaded["actual_price_usd"]
    author = json_loaded["author_1"]
    binding = json_loaded["binding_1"]
    dimensions = json_loaded["dimensions"]
    isbn = json_loaded["isbn13_1"]
    language = json_loaded["language"]
    image = json_loaded["media"][0]["path"]
    page_count = json_loaded["page_count"]
    publish_date = json_loaded["publish_date"]
    publisher = json_loaded["publisher"]
    title = json_loaded["title"]
    return {
        "title":title,
        "author":author,
        "price":price,
        "binding":binding,
        "ISBN":isbn,
        "publish date":publish_date,
        "publisher":publisher,
        "language":language,
        "page count":page_count,
        "dimension":dimensions,
        "image":image
    }


if __name__=="__main__":
    url = "https://bookoutlet.com/products/9781472853486B/soviet-pistols-tokarev-makarov-stechkin-and-others-weapon-bk-84"
    #html = open_browser(url)
    html = send_requests(url)
    #parse = parse_html(html)
    parse = parse_js(html)
    print(parse)