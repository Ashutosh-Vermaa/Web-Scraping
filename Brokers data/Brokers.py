
from selenium import webdriver

from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

import codecs

import re
import time
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.select import Select
import pandas as pd
import requests
from selenium.webdriver.common.by import By


DRIVER_PATH = "C/Users/Admin/Downloads/chromedriver_win32"
driver = webdriver.Chrome(executable_path=DRIVER_PATH)

driver.get('https://irdai.gov.in/list-of-brokers')

#extracting column names
response=driver.page_source
soup= BeautifulSoup(response,'html.parser' )


columns=[]
for i in (soup.find('tr').find_all('th')):
    columns.append(i.get_text())

#displaying 100 entries
select_element = Select(driver.find_element("name","brokersList_length"))  # Replace 'dropdown_id' with the actual ID of the dropdown element
select_element.select_by_value("100")  # Replace 'option_value' with the value of the option you want to select


data=[]
for i in range(7):
    
    response=driver.page_source
    soup= BeautifulSoup(response,'html.parser' )
    
    #extracting tags that contain records' data
    rows=soup.find('tbody').find_all('tr')
    
    #extracting data for each record 
    for row in rows:
        temp=[]
        #extracting data for each column fora record
        for i in row.find_all("td"):
            temp.append(i.get_text())
        data.append(temp)
    time.sleep(10)
    
    #going to the next page
    submit_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[id = 'brokersList_next']")))
    submit_button.click()
    # submit_button = driver.find_element('id','brokersList_next')  # Replace 'submit_button_id' with the actual ID of the submit button element
    # submit_button.click()

import pandas as pd
brokers=pd.DataFrame(data)
brokers.columns=columns

brokers.to_csv(f"C:/Users/Admin/Downloads/brokers.csv")
