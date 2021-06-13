# -*- coding: utf-8 -*-
import utils
import pandas
from datetime import datetime

def load_portfolio(date, price, length=10):
    d = utils.to_format(datetime(date.year, date.month, 1))
    try:
        data = pandas.read_csv("portfolio/high_update/%s.csv" % d, header=None)
        data.columns = ["code", "price", "count", "date"]
        data = data[data["price"] <= price]

        if len(data) < 50 or len(data) > 550:
            data = None
        else:
            data = data.iloc[:length]
    except:
        data = None
    return data

