# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 10:41:29 2021

@author: Timur Guler

Draft Script for Craigslist Seagull/Eastman Search
"""

# import packages
import pandas as pd
import numpy as np
import os
import requests
import json
from bs4 import BeautifulSoup

# function to extract html as  beatiful soup object given url and headers
def extract_html(url, headers=None):
    r = requests.get(url, headers = headers)
    result = BeautifulSoup(r.text, 'html')
    return result

# function to get results based on key
def conditional_bs4_results_key(bs, tag, result_key, condition_key, condition_value):
    '''
    Function to extract tag value from webscrape result if another key condition is met. Useful when a tag
    is used in multiple situations but is only relevant when other tag conditions are met
    
    Inputs:
    - bs: BeatifulSoup object containing the webscrape result
    - tag - tag used in main search
    - result_key - key whose result is to be extracted
    - condition_key - key which is sometimes present, and identifies relevant results when certain condition is met
    - condition_result - value of key when condition is met
    
    Outputs:
    - list of results
    '''
    output = []   
    for res in bs.find_all(tag):
        try:
            cond_actual = res[condition_key]
            if condition_value in list(cond_actual):
                output.append(res[result_key])
        except:
            pass
        
    return list(set(output))


# function to get results based on key
def conditional_bs4_results_text(bs, tag, condition_key, condition_value):
    '''
    Function to extract text value from webscrape result if another key condition is met. Useful when a tag
    is used in multiple situations but is only relevant when other tag conditions are met
    
    Inputs:
    - bs: BeatifulSoup object containing the webscrape result
    - tag - tag used in main search
    - condition_key - key which is sometimes present, and identifies relevant results when certain condition is met
    - condition_result - value of key when condition is met
    
    Outputs:
    - list of results
    '''
    output = []   
    for res in bs.find_all(tag):
        try:
            cond_actual = [res[condition_key]]
            if condition_value in cond_actual:
                output.append(res.text)
        except:
            pass
        
    return list(set(output))


def get_table(urls, headers=None):
    
    # set up lists to hold column values
    titles = []
    prices = []
    posteds = []
    updateds = []
    descriptions = []
    
    # loop through each potential guitar listing page
    for url in urls:
        
        # get searchable bs4 object
        result = extract_html(url, headers=headers)
        
        # get title
        title = conditional_bs4_results_text(result, 'span', 'id', 'titletextonly')[0]
        titles.append(title)
        
        # get price
        price = result.find_all('span', 'price')[0].text
        prices.append(price)
        
        # get all dates - min will be posting date, max will be updating date
        times = [res.text.replace('\n', '').strip() for res in result.find_all('time')]
        dates = pd.to_datetime(times).date
        
        posted = dates.min()
        updated = dates.max()
        
        posteds.append(posted)
        updateds.append(updated)
        
        # get body text description
        body = conditional_bs4_results_text(result, 'section', 'id', 'postingbody')[0]
        body = body.replace('QR Code Link to This Post', '').strip()
        
        descriptions.append(body)
    
    # create table
    table_dict = {'title' : titles,
                  'price' : prices, 
                  'posted' : posteds,
                  'updated' : updateds,
                  'body' : descriptions}
    
    # convert to pd
    output = pd.DataFrame(table_dict)
    return output

###########
# Main Section
###########


headers = {'user-agent' : 'Timur Guler search for seagull guitars tguler8@gmail.com'}
seagull_url = 'https://charlottesville.craigslist.org/d/musical-instruments/search/msa?query=seagull'
eastman_url = 'https://charlottesville.craigslist.org/d/musical-instruments/search/msa?query=eastman'

all_seagulls = extract_html(seagull_url, headers=headers)
all_eastmans = extract_html(eastman_url, headers=headers)

seagull_urls = conditional_bs4_results_key(all_seagulls, 'a', 'href', 'class', 'result-image')
eastman_urls = conditional_bs4_results_key(all_eastmans, 'a', 'href', 'class', 'result-image')

seagulls = get_table(seagull_urls, headers= headers)
eastmans = get_table(eastman_urls, headers= headers)


