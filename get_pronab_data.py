######################################################
# Author: Roshan M Regy
# Email ID:roshanm.regy@gmail.com
# Uses selenium and geckodriver (Firefox) to automate
# submission of PDB IDs to the ProNAB webserver
# containing protein-nucleic acid binding free 
# energy data 
#######################################################
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
import pandas as pd
import shutil
from time import sleep
from tqdm import trange
import sys

# Set options for the webdriver to run headless
options = Options()
options.headless = True
# URL for the main page of the database
url = "https://web.iitm.ac.in/bioinfo2/pronab/#Search"

# Read a list of PDB IDs to submit queries for 
data = pd.read_csv('pdbnames.csv')


t = trange(data.shape[0], desc='PDB ID ', leave=True)

for i in t:
    name = data['PDB'][i]
    t.set_description('PDB: %s' % name, refresh=True)
    flag = False
    while flag == False:
        print('Opening homepage...', end="")
        try:
            browser = webdriver.Firefox(
                options=options, executable_path='/usr/local/bin/geckodriver')
            browser.set_page_load_timeout(50)
            browser.get(url)
            flag = True
        except:
            browser.close()
            flag = False
    print('Ok')
    try:
        print('Opening search page...', end="")
        sleep(1)
        link = browser.find_element_by_link_text('Search')
        link.click()
    except:
        print('Opening search page...', end="")
        sleep(10)
        link = browser.find_element_by_link_text('Search')
        link.click()
    print('Ok')
    try:
        print('Entering PDB search query...', end="")
        sleep(1)
        pdbidinput = browser.find_element_by_name('PDB_complex_tx')
        pdbidinput.send_keys(name)
    except:
        print('Entering PDB search query...', end="")
        sleep(10)
        pdbidinput = browser.find_element_by_name('PDB_complex_tx')
        pdbidinput.send_keys(name)
    print('Ok')
    try:
        print('Submitting search query...', end='')
        button = browser.find_element_by_id("refresh")
        button.click()
    except:
        print('Submitting search query...', end='')
        sleep(20)
        button = browser.find_element_by_id("refresh")
        button.click()
    print('Ok')
    try:
        print('Downloading dataset...', end='')
        sleep(10)
        button = browser.find_element_by_name("insert")
        button.click()
        shutil.move('/home/abwer/Downloads/search_result.csv',
                    '/home/abwer/r.regy/dnaprobdb/%s_pronab.csv' % name)
        print('Ok')
    except:
        print('')
        print('%s No data in Pronab' % (name))
    browser.close()
