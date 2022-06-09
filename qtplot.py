# importing various libraries
import sys
from turtle import color
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import random
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
import pandas as pd

# calling the table from the database
cnx = sqlite3.connect('interfaces.db')

eth = pd.read_sql_query("SELECT * FROM eth", cnx)
lo = pd.read_sql_query("SELECT * FROM lo", cnx)
wlan = pd.read_sql_query("SELECT * FROM wlan", cnx)

eth['inutilize'] = ( eth['ifInoctets'].diff() * 800 ) / 5000000000
eth['outtilize'] = ( eth['ifOutoctets'].diff() * 800 ) / 5000000000

lo['inutilize'] = ( lo['ifInoctets'].diff() * 800 ) / 5000000000
lo['outtilize'] = ( lo['ifOutoctets'].diff() * 800 ) / 5000000000

wlan['inutilize'] = ( wlan['ifInoctets'].diff() * 800 ) / 5000000000
wlan['outtilize'] = ( wlan['ifOutoctets'].diff() * 800 ) / 5000000000

eth_inutilize_lst = eth['inutilize'][1:].to_list()
eth_outtilize_lst = eth['outtilize'][1:].to_list()

lo_inutilize_lst = lo['inutilize'][1:].to_list()
lo_outtilize_lst = lo['outtilize'][1:].to_list()

wlan_inutilize_lst = wlan['inutilize'][1:].to_list()
wlan_outtilize_lst = wlan['outtilize'][1:].to_list()

elements = len(eth)-1 
# main window
# which inherits QDialog
class Window(QDialog):
	
	# constructor
	def __init__(self, parent=None):
		super(Window, self).__init__(parent)

		# a figure instance to plot on
		self.figure = plt.figure()

		# this is the Canvas Widget that
		# displays the 'figure'it takes the
		# 'figure' instance as a parameter to __init__
		self.canvas = FigureCanvas(self.figure)

		# this is the Navigation widget
		# it takes the Canvas widget and a parent
		self.toolbar = NavigationToolbar(self.canvas, self)

		# Just some button connected to 'plot' method
		self.button = QPushButton('Plot')
		
		# adding action to the button
		self.button.clicked.connect(self.plot)

		# creating a Vertical Box layout
		layout = QVBoxLayout()
		
		# adding tool bar to the layout
		layout.addWidget(self.toolbar)
		
		# adding canvas to the layout
		layout.addWidget(self.canvas)
		
		# adding push button to the layout
		layout.addWidget(self.button)
		
		# setting layout to the main window
		self.setLayout(layout)

	# action called by the push button
	def plot(self):

		# clearing old figure
		self.figure.clear()

		# create an axis
		ax = self.figure.add_subplot(111)

		x = np.linspace(0, 10, elements)  # Sample data.
		# print(x)

		# Note that even in the OO-style, we use `.pyplot.figure` to create the Figure.
		# ax = plt.subplots(figsize=(5, 2.7), layout='constrained')
		ax.plot(x, eth_inutilize_lst,  label='eth input utilization')  # Plot some data on the axes.
		ax.plot(x, eth_outtilize_lst,  linestyle='--', label='eth output utilization')  # Plot more data on the axes...
		ax.plot(x, lo_inutilize_lst,  label='lo input utilization')  # Plot some data on the axes.
		ax.plot(x, lo_outtilize_lst,  linestyle='--', label='lo output utilization')  # Plot more data on the axes...
		ax.plot(x, wlan_inutilize_lst,  label='wlan input utilization')  # Plot some data on the axes.
		ax.plot(x, wlan_outtilize_lst,  linestyle='--', label='wlan output utilization')  # Plot more data on the axes...
		ax.set_xlabel('time')  # Add an x-label to the axes.
		ax.set_ylabel('utilization')  # Add a y-label to the axes.
		ax.set_title("all interface")  # Add a title to the axes.
		ax.legend();  # Add a legend.
		# refresh canvas
		self.canvas.draw()

# driver code
if __name__ == '__main__':
	
	# creating apyqt5 application
	app = QApplication(sys.argv)

	# creating a window object
	main = Window()
	
	# showing the window
	main.show()

	# loop
	sys.exit(app.exec_())
