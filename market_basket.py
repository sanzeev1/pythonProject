#!/usr/bin/env python
# coding: utf-8

# # Implementing market basket analysis

# In[1]:


# Loading neccesary packages
import json

import numpy as np
import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules


# converting all positive values to 1 and everything else to 0
def my_encode_units(x):
    if x <= 0:
        return 0
    if x >= 1:
        return 1


def marketBasket(min_support, country):
    waitHtml = '<meta http-equiv="refresh" content="30; URL=http://127.0.0.1:5000/output">' \
               '<h1>Your job is currently processing. Please check after  sometime.</h1>'
    file = open("template/output.html", "w")
    file.write(waitHtml)
    file.close()
    # Reading Data From Web
    print('fetching data')
    myretaildata = pd.read_excel('http://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx')
    print(myretaildata.shape)

    print('data fetched successfully')
    # # Data Preparation
    # Data Cleaning
    myretaildata['Description'] = myretaildata['Description'].str.strip()  # removes spaces from beginning and end
    myretaildata.dropna(axis=0, subset=['InvoiceNo'], inplace=True)  # removes duplicate invoice
    myretaildata['InvoiceNo'] = myretaildata['InvoiceNo'].astype('str')  # converting invoice number to be string
    myretaildata = myretaildata[~myretaildata['InvoiceNo'].str.contains('C')]  # remove the credit transactions

    print(myretaildata['Country'].value_counts())
    # myretaildata.shape

    # Separating transactions for Germany
    mybasket = (myretaildata[myretaildata['Country'] == country]
                .groupby(['InvoiceNo', 'Description'])['Quantity']
                .sum().unstack().reset_index().fillna(0)
                .set_index('InvoiceNo'))

    # viewing transaction basket

    my_basket_sets = mybasket.applymap(my_encode_units)
    my_basket_sets.drop('POSTAGE', inplace=True, axis=1)  # Remove "postage" as an item

    # # Training Model
    # Generating frequent itemsets
    my_frequent_itemsets = apriori(my_basket_sets, min_support=float(min_support), use_colnames=True)

    # generating rules
    my_rules = association_rules(my_frequent_itemsets, metric="lift", min_threshold=1)

    # # Making recommendations

    print(my_basket_sets['ROUND SNACK BOXES SET OF4 WOODLAND'].sum())

    print(my_basket_sets['SPACEBOY LUNCH BOX'].sum())

    # Filtering rules based on condition
    df = (my_rules[(my_rules['lift'] >= 3) &
                   (my_rules['confidence'] >= 0.3)])
    df = (df.to_html())
    print(df)
    file = open("template/output.html", "w")
    file.write(df)
    file.close()

# print('running market basket')
# marketBasket()
