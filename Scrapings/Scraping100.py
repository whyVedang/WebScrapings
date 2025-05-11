import pandas as pd
import numpy as np
pd.set_option('display.max_columns', None) 
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', 100)   
URL="https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29"
tables = pd.read_html(URL)
print(tables)
table = tables[3]
table.columns = range(table.shape[1])
table=table[[0,2]]
table=table[0:11]
table.columns = ['Country', 'GDP']
table['GDP']=(table[['GDP']].astype(int))/1000
table[['GDP']]=np.round(table[['GDP']],2)
print(table)
table.to_csv('./Largest_economies.csv')