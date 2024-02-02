import concurrent.futures

from product_details import read_file_to_links,send_requests,parse_js,save_to_excel


def main(url):
    html = send_requests(url)    
    product_details = parse_js(html)
    result.append(product_details)
    print(f"Getting {len(result)} of result")

if __name__=="__main__":

    result = []

    all_links = read_file_to_links("final_links.txt")
    try: 
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(main,all_links)
    except Exception:
        print(Exception)
    finally:
        save_to_excel(result)

"""
for 99 of url
in the synchronous version we got 2 minutes
in the concurrent version
user    0m34,571s
for 8180 data:
user    44m28,776s

all data success scraped
improved by using context manager in request saving ram
total in 279 minutes / 4.5 hours for 50k+ data

to be learn
https://curl-cffi.readthedocs.io/en/latest/#features

"""