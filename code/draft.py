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

# set craigslist url

headers = {'user-agent' : 'Timur Guler search for seagull guitars tguler8@gmail.com'}
url = 'https://charlottesville.craigslist.org/d/musical-instruments/search/msa?query=seagull'

r = requests.get(url, headers = headers)
result = BeautifulSoup(r.text, 'html')

# function to get results based on key
def conditional_bs4_results(bs, tag, result_key, condition_key, condition_value):
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
        
    return set(output)

seagull_urls = conditional_bs4_results(result, 'a', 'href', 'class', 'result-image')

# Next steps
# look at listing pages and determine how to best extract info
# extract info from pages and put into table


