from sqlalchemy import create_engine

import sqlite3
import json
import pandas


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


if __name__=="__main__":
    read_excel_to_sqlite("final_result.xlsx")