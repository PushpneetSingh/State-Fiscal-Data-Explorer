import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import requests
import time

# EXTRACT

url = 'https://himkosh.nic.in/eHPOLTIS/PublicReports/wfrmBudgetAllocationbyFD.aspx'
# Hard coded date for now but can use datetime functions to populate dynamic values
strt_d = '01/04/2018' 
end_d = '31/03/2022'

# setting up seleium driver
ops = webdriver.ChromeOptions()
ops.add_argument("headless")
web=webdriver.Chrome(options=ops)
web.get(url)

# 1 second pause to fill data just to not block our ip address ;-)
time.sleep(1)

web.execute_script("document.getElementById('txtFromDate').setAttribute('value', arguments[0])",strt_d)
time.sleep(1)
web.execute_script("document.getElementById('txtQueryDate').setAttribute('value', arguments[0])",end_d)
#HOA is by default, so skipping that
time.sleep(1)
web.find_element(By.ID,"MainContent_rbtUnit_0").click()
time.sleep(1)
web.find_element(By.ID,"btnGetdata").click()

time.sleep(4)

soup = BeautifulSoup(web.page_source, "html.parser")

table = soup.find('table')

data = []
table_body = table.find('tbody')

rows = table_body.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append(cols)

# header info
header=[]
table_head = table.find('thead')

rows = table_head.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    #'=' instead of append because we only need last row data in 'thead' 
    header=cols

# Converting to data frame and storing to data lake (For now Data Lake is my computer C drive ;-) )
df = pd.DataFrame(data, columns=header)
df.to_csv('../data/HP_financial_raw_data.csv')

# web.quit()
