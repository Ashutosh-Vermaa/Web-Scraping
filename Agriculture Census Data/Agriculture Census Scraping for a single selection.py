
from selenium import webdriver

from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

import codecs

import re

from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.select import Select
import pandas as pd
import requests

DRIVER_PATH = "C/Users/Admin/Downloads/chromedriver_win32"
driver = webdriver.Chrome(executable_path=DRIVER_PATH)

driver.get('https://agcensus.dacnet.nic.in/DistCharacteristic.aspx')


select_element = Select(driver.find_element("id","_ctl0_ContentPlaceHolder1_ddlYear"))  # Replace 'dropdown_id' with the actual ID of the dropdown element
select_element.select_by_value("1995")  # Replace 'option_value' with the value of the option you want to select

select_element = Select(driver.find_element("id","_ctl0_ContentPlaceHolder1_ddlSocialGroup"))
select_element.select_by_value("1")

select_element = Select(driver.find_element("id","_ctl0_ContentPlaceHolder1_ddlState"))
select_element.select_by_value("11a")


select_element = Select(driver.find_element("id","_ctl0_ContentPlaceHolder1_ddlDistrict"))
select_element.select_by_value("9")

select_element = Select(driver.find_element("id","_ctl0_ContentPlaceHolder1_ddlTables"))
select_element.select_by_value("3")

submit_button = driver.find_element('id','_ctl0_ContentPlaceHolder1_btnSubmit')  # Replace 'submit_button_id' with the actual ID of the submit button element
submit_button.click()



response=driver.page_source

soup= BeautifulSoup(response,'html.parser' )
soup.find('table').find('tbody').find_all('tr', attrs={'valign':"top"})[7].get_text()

data=soup.find('table').find('tbody').find_all('tr', attrs={'valign':"top"})

tab1=[]

for rec in data[8:-1]:
    temp=[]
    for i in rec.find_all('div'):
        temp.append(i.get_text())
    tab1.append(temp)

df1=pd.DataFrame(tab1)

print(df1)
# url = driver.current_url



# driver.get(url)

# page_source= driver.page_source





# soup.find('table').find('tbody').find_all('tr', attrs={'valign':"top"})[8].get_text()