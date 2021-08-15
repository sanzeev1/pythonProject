import csv
import json
from threading import Thread


from flask import Flask, render_template, request, redirect
import pandas as pd
import numpy as np
from numpy import matrix
# from mlxtend.frequent_patterns import apriori
# from mlxtend.frequent_patterns import association_rules
# from werkzeug.datastructures import RequestCacheControl
from market_basket import marketBasket

app = Flask(__name__, template_folder='template')
# myretaildata = pd.read_excel('http://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx')


@app.route('/')
def index():
    title = "Learning New"
    return render_template('index.html', title=title)


@app.route('/about')
def about():
    names = ["Ram", "Shyam", "Hari"]
    return render_template('about.html', names=names)


@app.route('/form', methods=['POST'])
def form():
    # support = RequestCacheControl.form.get('support')
    return render_template('form.html')


@app.route('/start', methods=['POST'])
def start():
    support = request.form.get('support', 0.01)
    print(support)
    c = request.form.get('country', 'Germany')

    def do_work(min_support, country):
        marketBasket(min_support, country)

    thread = Thread(target=do_work, kwargs={'min_support': support, 'country': c})
    thread.start()
    return redirect('/output')


@app.route('/output', methods=['GET'])
def output():
    file = open("template/output.html", "r")
    content = file.read()
    file.close()
    return render_template('output_main.html', content=content)


@app.route('/startForm', methods=['GET'])
def startForm():
    array = []

    with open("country.txt") as f:
        data = f.readlines()
        for row in data:
            array.append(row)
            # print(row.rstrip())

        print(array)
    return render_template('response.html', arr=array)
