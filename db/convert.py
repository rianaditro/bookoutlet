import pandas


def read_excel_to_html(filename):
    df = pandas.read_excel(filename)
    html = df.to_html()
    return html
    