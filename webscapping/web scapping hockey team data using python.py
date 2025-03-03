from bs4 import BeautifulSoup
import requests
import pandas as pd
url="https://www.scrapethissite.com/pages/forms/"
page=requests.get(url)
soup=BeautifulSoup(page.text,'lxml')
table=soup.find_all('table')
header=soup.find_all('th')
title=[title.text.strip() for title in header]
df=pd.DataFrame(columns=title)
col_row=soup.find_all('tr')
for rows in col_row[1:]:
    row=rows.find_all('td')
    data=[data.text.strip() for data in row]
    length=len(df)
    df.loc[length]=data

print(df)
df.to_csv(r'C:\Users\Safia\Desktop\work\pthon projects\hockey_teams.csv',index=False)
