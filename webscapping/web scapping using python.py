from bs4 import BeautifulSoup
import requests
import pandas as pd
url="https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue"
page=requests.get(url)
soup=BeautifulSoup(page.text,'lxml')
table=soup.find_all('table')[0]
header=table.find_all('th')
title=[title.text.strip() for title in header]
df=pd.DataFrame(columns=title)
print(df)
col_rows=table.find_all('tr')
#print(col_rows)
for row in col_rows[1:]:
    row_data=row.find_all('td')
    r=[data.text.strip() for data in row_data]
    length=len(df)
    df.loc[length]=r

print(df)
df.to_csv(r'C:\Users\Safia\Desktop\work\pthon projects\companies.csv',index=False)



