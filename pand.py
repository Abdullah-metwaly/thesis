import sqlite3
import pandas as pd
cnx = sqlite3.connect('interfaces.db')

df = pd.read_sql_query("SELECT * FROM eth", cnx)

print(df)

df['inutilize'] = ( df['ifInoctets'].diff() * 800 ) / 5000000000
df['outtilize'] = ( df['ifOutoctets'].diff() * 800 ) / 5000000000

inutilize_lst = df['inutilize'][1:].to_list()
outtilize_lst = df['outtilize'][1:].to_list()

print(inutilize_lst)
print(outtilize_lst)