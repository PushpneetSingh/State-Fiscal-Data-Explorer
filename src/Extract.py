import pandas as pd
import numpy as np
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
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
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--remote-allow-origins=*')

web = webdriver.Chrome(options=options)
web.get(url)

# 3 second pause to fill data just to not block our ip address ;-)
time.sleep(3)

#wait = WebDriverWait(web, 20)  # Adjust the timeout as needed
#web.execute_script("arguments[0].setAttribute('value', arguments[1])", wait.until(EC.visibility_of_element_located((By.ID, 'txtFromDate'))), strt_d)


web.execute_script("document.getElementById('txtFromDate').setAttribute('value', arguments[0])", strt_d)
web.execute_script("document.getElementById('txtQueryDate').setAttribute('value', arguments[0])",end_d)
#HOA is by default, so skipping that
time.sleep(1)
web.find_element(By.ID,"MainContent_rbtUnit_0").click()
time.sleep(1)
web.find_element(By.ID,"btnGetdata").click()

time.sleep(4)

soup = BeautifulSoup(web.page_source, "html.parser")

# Extracting table details

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
df.to_csv('$AIRFLOW_HOME/data/HP_financial_raw_data.csv')

web.quit()
