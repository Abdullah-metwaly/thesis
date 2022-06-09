import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
import pandas as pd
cnx = sqlite3.connect('interfaces.db')


df = pd.read_sql_query("SELECT * FROM lo", cnx)

# print(df)

df['inutilize'] = ( df['ifInoctets'].diff() * 800 ) / 5000000000
df['outtilize'] = ( df['ifOutoctets'].diff() * 800 ) / 5000000000

inutilize_lst = df['inutilize'][1:].to_list()
outtilize_lst = df['outtilize'][1:].to_list()


x = np.linspace(0, 60, 13 )  # Sample data.
# print(x)

# Note that even in the OO-style, we use `.pyplot.figure` to create the Figure.
fig, ax = plt.subplots(figsize=(5, 2.7), layout='constrained')
ax.plot(x, inutilize_lst, label='input utilization')  # Plot some data on the axes.
ax.plot(x, outtilize_lst, label='output utilization')  # Plot more data on the axes...
ax.set_xlabel('x label')  # Add an x-label to the axes.
ax.set_ylabel('y label')  # Add a y-label to the axes.
ax.set_title("Simple Plot")  # Add a title to the axes.
ax.legend();  # Add a legend.

plt.show()