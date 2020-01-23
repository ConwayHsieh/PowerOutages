import requests
import pandas as pd
from bs4 import BeautifulSoup
from tabulate import tabulate
url = 'https://en.wikipedia.org/wiki/List_of_California_locations_by_income'
website_url = requests.get(url).text
soup = BeautifulSoup(website_url,'lxml')
#print(soup.prettify())
My_table = soup.findAll('table',{'class':'wikitable sortable'})
#print(My_table[1])
df = pd.read_html(str(My_table[1]))[0]
#print(type(df))
print( tabulate(df, headers='keys', tablefmt='psql') )
df.to_csv('california_pop_income.csv', index=False)

