from sqlalchemy import create_engine

import sqlite3
import json
import pandas


class BookExcel(object):
    def __init__(self, title, author, price, binding, 
                 isbn, publisher_date, publisher, language, 
                 page_count, dimension, image):
        self.title = title
        self.author = author
        self.price = price
        self.binding = binding
        self.isbn = isbn
        self.publisher_date = publisher_date
        self.publisher = publisher
        self.language = language
        self.page_count = page_count
        self.dimension = dimension
        self.image = image

def excel_to_object(filename):
    df = pandas.read_excel(filename)
    df_to_list = df.values.tolist()
    df_instances = []
    for df_ in df_to_list:
        df_instances.append(BookExcel(*df_))
    
    return df_instances


def read_excel_to_html(filename):
    df = pandas.read_excel(filename)
    html = df.to_html()
    return html
    
def read_excel_to_sql(filename):
    df = pandas.read_excel(filename)
    engine = create_engine("sqlite:///bookoutlet.db",echo=False)
    df.to_sql("booksTable",con=engine)

def read_excel_to_sqlite(filename):
    df = pandas.read_excel(filename)
    conn = sqlite3.connect("db/bookoutlet.sqlite")
    df.to_sql("bookTable",conn,if_exists="replace")
    conn.close()

def get_db(filename):
    db = sqlite3.connect(filename)
    db.row_factory = sqlite3.Row
    return db

def excel_to_dict():
    df = pandas.read_excel("final_result.xlsx")
    datas = df.to_json(index=False)
    products = json.loads(datas)
    print(products)
