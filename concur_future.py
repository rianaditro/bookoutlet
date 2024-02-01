import concurrent.futures

from product_details import read_file_to_links,send_requests,parse_js,save_to_excel


def main(url):
    html = send_requests(url)    
    product_details = parse_js(html)
    result.append(product_details)

if __name__=="__main__":

    result = []

    all_links = read_file_to_links("final_links.txt")[1:100]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(main,all_links)

    save_to_excel(result)

"""
for 99 of url
in the synchronous version we got 2 minutes
in the concurrent version
user    0m34,571s

to be learn
https://curl-cffi.readthedocs.io/en/latest/#features

next to do is experimenting if this shit is blocked or not
"""