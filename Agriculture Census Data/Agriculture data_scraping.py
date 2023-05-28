#Extracting the values of Social Groups

import requests
from bs4 import BeautifulSoup

response=requests.get("https://agcensus.dacnet.nic.in/DistCharacteristic.aspx")
soup= BeautifulSoup(response.text,'html.parser')

groups=soup.find("select", attrs={"id":"_ctl0_ContentPlaceHolder1_ddlSocialGroup"}).find_all("option")

social_groups=[]
for grp in groups:
    social_groups.append(grp['value'])
    
################ Manually the values of Districts###################

districts=[9,15,17,7,8,16,14,18,20,6,19,21,10,3,4,13,12,5,11,2]

### IMPORTS

from selenium import webdriver

from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup


from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.select import Select
import pandas as pd
import requests

DRIVER_PATH = "C/Users/Admin/Downloads/chromedriver_win32"
driver = webdriver.Chrome(executable_path=DRIVER_PATH)

all_tables=[]
for social in social_groups:
    for district in districts:
        

        driver.get('https://agcensus.dacnet.nic.in/DistCharacteristic.aspx')
        
        
        select_element = Select(driver.find_element("id","_ctl0_ContentPlaceHolder1_ddlYear"))  # Replace 'dropdown_id' with the actual ID of the dropdown element
        select_element.select_by_value("1995")  # Replace 'option_value' with the value of the option you want to select
        
        select_element = Select(driver.find_element("id","_ctl0_ContentPlaceHolder1_ddlSocialGroup"))
        select_element.select_by_value(social)
        
        select_element = Select(driver.find_element("id","_ctl0_ContentPlaceHolder1_ddlState"))
        select_element.select_by_value("11a")
        
        
        ######################
        ################Extracting the values of Districts###################
        
        # response=driver.find_element("id","_ctl0_ContentPlaceHolder1_ddlDistrict")
        
        # district=response.get_attribute('option')
        
        # districts=[]
        # for grp in district:
        #     districts.append(grp.get_attribute('option'))
        ################################
        
        
        select_element = Select(driver.find_element("id","_ctl0_ContentPlaceHolder1_ddlDistrict"))
        select_element.select_by_value(str(district))
        
        select_element = Select(driver.find_element("id","_ctl0_ContentPlaceHolder1_ddlTables"))
        select_element.select_by_value("3")
        
        submit_button = driver.find_element('id','_ctl0_ContentPlaceHolder1_btnSubmit')  # Replace 'submit_button_id' with the actual ID of the submit button element
        submit_button.click()
        
        
        
        response=driver.page_source
        
        soup= BeautifulSoup(response,'html.parser' )
        # soup.find('table').find('tbody').find_all('tr', attrs={'valign':"top"})[7].get_text()
        try:
            data=soup.find('table').find('tbody').find_all('tr', attrs={'valign':"top"})
        
        except:
            continue
        
        tab1=[]
        
        for rec in data[8:-1]:
            temp=[]
            for i in rec.find_all('div'):
                temp.append(i.get_text())
            tab1.append(temp)
        
        df=pd.DataFrame(tab1)
        df.to_csv(f"C:/Users/Admin/Downloads/Scraped _data/{social}_{district}.csv")
        
        # all_tables.append(tab1)



# df0=pd.DataFrame(all_tables[0])


# df0.to_csv(f"C:/Users/Admin/Downloads/Scraped _data/{district}_{social}.csv")

# i=0
# for j in range(len(all_tables[20])):
#     df=pd.DataFrame(all_tables[j])
    
#     df.to_csv(f"C:/Users/Admin/Downloads/Scraped _data/Scheduled Caste/{districts[i]}.csv")
#     i+=1
#     print("done")
    

#         # df1=pd.DataFrame(tab1)
        
#         # print(df1)
# # url = driver.current_url



# # driver.get(url)

# # page_source= driver.page_source





# # soup.find('table').find('tbody').find_all('tr', attrs={'valign':"top"})[8].get_text()