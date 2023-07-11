
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

# Create a new excel workbook

name_list=["lifeinsurers_length", "nonlifeinsurers_length", "healthl_length",
            "reinsurers_length", "reinsurersbranches_length","agentList_length",
            "telemarkters_length",
            "brokersList_length","marketingfirms_length", "surveyorsList_length",
            "directorPartnersurveyors_length",
            "insurancerepositories_length","thirdpartyadmins_length",
            "webaggregators_length"]

DRIVER_PATH = "C/Users/Admin/Downloads/chromedriver_win32"
driver = webdriver.Chrome(executable_path=DRIVER_PATH)

driver.get('https://irdai.gov.in/list-of-brokers')
response=driver.page_source

soup= BeautifulSoup(response,'html.parser' )

#extracting links to insurers
insurer= soup.find("ul", {"class": "claim-list"}).find_all("a")
insurer_links=[]
for i in insurer:
    insurer_links.append(i["href"])
    
del insurer_links[6]
del insurer_links[-7]
del insurer_links[-4]

hmap={}
n=0
for link in insurer_links:
    driver.get(link)
    
    #displaying 100 entries
    select_element = Select(driver.find_element("name",name_list[n]))  # Replace 'dropdown_id' with the actual ID of the dropdown element
    select_element.select_by_value("100")  # Replace 'option_value' with the value of the option you want to select
    
    response=driver.page_source
    soup= BeautifulSoup(response,'html.parser' )
    columns=[]
    for i in (soup.find('tr').find_all('th')):
        columns.append(i.get_text())
    
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
        try:
        #going to the next page
            submit_button = driver.find_element('id',name_list[n][:-7]+"_next")  # Replace 'submit_button_id' with the actual ID of the submit button element
            submit_button.click()        
            # submit_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[id = name_list[n][:-7]]")))
            # submit_button.click()
        except:
            break
        # submit_button = driver.find_element('id','brokersList_next')  # Replace 'submit_button_id' with the actual ID of the submit button element
        # submit_button.click()
    n+=1
    brokers=pd.DataFrame(data)
    brokers.columns=columns
    hmap[f"{name_list[n-1][:-7]}"]=brokers

writer = pd.ExcelWriter(f"C:/Users/Admin/Downloads/insurers1.xlsx", engine='xlsxwriter')
for key, val in hmap.items():
# Write each dataframe to a different worksheet.
# data1.to_excel(writer, sheet_name="data1",  index=False)
# data2.to_excel(writer, sheet_name="data2",  index=False)
# # Save the Excel file

#     # brokers.to_csv(f"C:/Users/Admin/Downloads/brokers.csv")
    hmap[key].to_excel(writer, sheet_name=key,  index=False)
writer.save()  