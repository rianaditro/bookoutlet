from bs4 import BeautifulSoup
from all_product_links import read_file_to_links

import cloudscraper,json,pandas


def send_requests(url):
    with cloudscraper.create_scraper() as scraper:
        resp = scraper.get(url)
        print(f"getting {resp.status_code} from {url}")
        resp = resp.text
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

def main():
    result = []
    all_links = read_file_to_links("final_links.txt")
    # all data available up to 52000. The first 100 data need 2 minutes
    #improve this
    for links in all_links[1:100]:
        html = send_requests(links)
        parse = parse_js(html)
        result.append(parse)
    return result

def save_to_excel(result):
    df = pandas.DataFrame(result)
    df.to_excel("final_result.xlsx",index=False)

if __name__=="__main__":
    result = main()
    save_to_excel(result)