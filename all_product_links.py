# read all product links that already scraped before

def read_file_to_links(filename)->set():
    with open(filename,"r",encoding="utf-8") as f:
        text = f.read()
        text = list(text.split("https://bookoutlet.com/products/"))

        set_link = set()
        for link in text:
            set_link.add(f"https://bookoutlet.com/products/{link}")
        return list(set_link)
    
if __name__=="__main__":
    set_link = read_file_to_links("final_links.txt")
    print(set_link[1:100])
    print(len(set_link))