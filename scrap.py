from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import cloudscraper, re, time
from bs4 import BeautifulSoup

def get_html(url:str):
    scraper = cloudscraper.CloudScraper()
    headers = {'Accept': 'text/html'}
    response = scraper.get(url,headers=headers)
    time.sleep(1)
    html = response.text
    soup = BeautifulSoup(html,"html.parser")
    return soup

def get_categories(soup:BeautifulSoup):
    result = dict()
    items = soup.find_all("h5","MuiTypography-root MuiTypography-h5")
    categories = [item.text for item in items]
    for item in categories[:5]:
        i = item.split()
        join = "%20".join(i).lower()
        url = f"https://bookoutlet.com/browse/products/{join}"
        result[item] = url
    return result

def how_many_pages(soup:BeautifulSoup):
    pages = soup.find("p","MuiTypography-root MuiTypography-body1 MuiTypography-alignCenter").text
    match = re.search(r"of (\d+)",pages)
    if match:
        result = match.group(1)
    if int(result) < 5:
        return int(result)
    else:
        return 3

def get_all_url(soup:BeautifulSoup):
    book_urls = set()
    items = soup.find_all("div","MuiGrid-root MuiGrid-item MuiGrid-grid-xs-6 MuiGrid-grid-sm-4 MuiGrid-grid-md-4 MuiGrid-grid-lg-3")
    for item in items:
        url = item.find("a")["href"]
        book_urls.add(url)
    return book_urls

def get_html_per_product(url:str):
    #product page need to click button in order to get additional info
    options = Options()
    options.add_argument("--enable-javascript")
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options)
    driver.get(url)
    time.sleep(3)
    
    try:
        # I Agree Button
        driver.find_element(By.XPATH,'//*[@id="cookieBanner"]/div/button').click()
        # Additional Info Button
        driver.find_element(By.XPATH,'//*[@id="main"]/main/div/div/div/div[4]/button[1]').click()
    except:
        pass

    html = driver.page_source
    return html

def html_to_product_data(html):
    soup = BeautifulSoup(html,"html.parser")

    title = soup.find("h1","MuiTypography-root MuiTypography-h1").text

    p = soup.find_all("p")
    # valueable p in range 5 to 15
    author = p[5].text.replace("by ","")
    format_book = p[6].text
    price = p[7].text.replace("$","")
    price = get_string(price)
    stock = get_string(p[8].text)
    isbn = get_string(p[10].text)
    pub_date = get_string(p[11].text)
    publisher = get_string(p[12].text)
    language = get_string(p[13].text)
    page_count = get_string(p[14].text)
    size = get_string(p[15].text)  

    result = {
        "title":title,
        "author":author,
        "format":format_book,
        "price":price,
        "stock":stock,
        "ISBN":isbn,
        "publish date":pub_date,
        "publisher":publisher,
        "language":language,
        "page count":page_count,
        "size":size
    }
    return result

def get_string(text):
    pattern = r': (.+)'
    match = re.search(pattern,text)

    if match:
        result = match.group(1)
    else:
        result = text
    return result

def save_to_local(content,filename:str="output.txt"):
    with open(filename,"w",encoding="utf-8") as file:
        file.write(', '.join(content))
        file.close()
    print(f"File saved to {filename}")
        


def main():
    url_all_books = set()

    main_url = "https://bookoutlet.com/categories"

    soup = get_html(main_url)
    categories = get_categories(soup)
    """{"category name":category url}"""
    for category in categories:
        print(f"Bookoutlet-category:{category}")
        url = categories[category]
        pagination = "?page="
        soup = get_html(url)
        count_page = how_many_pages(soup)
        for counter in range(1,count_page+1):
            print(f"Getting page {counter} of {count_page}")
            try:
                url_page = f"{url}{pagination}{counter}"
                soup = get_html(url_page)
                url_books = get_all_url(soup)
                url_all_books.update(url_books)
                print(len(url_all_books))
            except Exception as e:
                print(f"{e} on {url_page}")
    save_to_local(url_all_books,"all_books_url.txt","txt")


if __name__=="__main__":
    result = []
    with open("all_books_url.txt","r",encoding="utf-8") as file:
        urls = file.read()
        file.close()
    urls = urls.split(",")
    for url in urls:
        html = get_html_per_product(url)
        product_data = html_to_product_data(html)
        product_data["URL"]=url
        result.append(product_data)
    save_to_local(result,"scrap_result.txt","txt")