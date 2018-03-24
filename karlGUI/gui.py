# Karl Preisner
# 7 March 2018

""" 
Current version:
- check list controls dynamic visibility of fields
"""

# Reference for downloaded icon:
# <div>Icons made by <a href="http://www.freepik.com" title="Freepik">Freepik</a> 
# from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a> 
# is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" title="Creative 
# Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>

# tkinter stuff
from tkinter import *
import tkinter as tk
from tkinter.ttk import *
from VerticalScrolledFrame import *

# other stuff
import time, random, math, threading

# Important development tips:
#   - To add a widget to a VerticalScrolledFrame v, you must use 'v.interior'
#     Example: Label(self.v.interior, text="hello")

"""
TODO:
* arrow keys/scroll wheel for navigation
* go to specific page in page navigation
* search bar
* edit record button
* Add dataEntry
	- update self.numRecords, self.numRecordsLabel upon save of entry
* separate gui and database access functions into multiple files
"""

import os

class GUI:
	def __init__(self, master):
		self.master = master

		# Set Window Title
		self.master.title("Fossile Data Entry")
		# Set Window Dimensions
		# self.master.minsize(width = 600, height = 400)
		# self.master.maxsize(width = 600, height = 400)
		self.master.geometry('800x600')

		self.getFields()

		# GUI settings
		self.recordsPerPage = 50 # if more than 50 and rendering is SLOW

		# Class Variables
		self.pageNum = 0 # Which page of self.dataList are we looking at
		self.numRecords = 115

		self.createEasyDatabase() # fake database for testing gui
		self.getListViewFields() # get config file settings for list view

		# draw main page
		self.drawMainPage()


	def getListViewFields(self):
		# Get all fields selected to be shown in listView

		# TODO: Retrieve from config file
		# field is a tuple: ("name", number of characters to be displayed)
		self.listViewFields = [
			("ID",6),("Name",10),
			("Qty",6),("x",10),
			("y",10),("Date Created",16),
			("Last Modified",16)]

		self.listViewFields = [
			("ID",6),("Name",10),
			("Qty",6),("Date Created",16),
			("Last Modified",16),("Color",10),("ID",6)]

	def getFields(self):
		# Get all fields defined in config file.
		# All of these fields will be shown in dataEntryTab.
		x = SimpleRecord(-1)
		self.fields = []
		for key,value in x.fields.items():
			self.fields.append(key)

	# This method calls the other draw methods
	def drawMainPage(self):
		self.drawNoteBook()
		self.drawListViewTab()
		# self.drawDataEntryTab() # BUG!!!!!!!! Runtime error (freeze)!!!!
		self.populateDataList()

	def drawNoteBook(self):
		# Create notebook (it is a frame that with multiple tabbed windows)
		self.notebook = Notebook(self.master)

		# Tabs in the notebook. 
		self.listViewTab = Frame(self.notebook)
		self.dataEntryTab = Frame(self.notebook)
		self.notebook.add(self.listViewTab, text = "List View")
		self.notebook.add(self.dataEntryTab, text = "Data Entry")

		# Draw the notebook
		self.notebook.pack(side=TOP,fill=BOTH,expand=True)
		Label(self.dataEntryTab,text="Enter data here. This will create a new\nrow in the list view with a unique ID.").pack()

	def drawListViewTab(self):
		# for widget in self.listViewTab.winfo_children():
		# 	widget.destroy()

		# Create the container frames in the list view tab
		self.columnNames = Frame(self.listViewTab)
		self.dataList = VerticalScrolledFrame(self.listViewTab)
		self.navFooter = Frame(self.listViewTab)
		# draw the containers
		self.columnNames.pack(fill=X)
		Separator(self.listViewTab, orient="horizontal").pack(fill=X) # separator line
		self.dataList.pack(fill=BOTH,expand=True)
		Separator(self.listViewTab, orient="horizontal").pack(fill=X) # separator line
		self.navFooter.pack(fill=X)

		# fill the containers
		self.drawColumnNames()
		self.drawRecordRows()
		self.drawNavFooter()

	def drawDataEntryTab(self):
		f = ('Times',14,'bold') # font for column names
		for row, field in enumerate(self.fields): # num columns (fields)
			Label(self.dataEntryTab,text=field,width=10,font=f).grid(row=row,column=0,pady=10,padx=10)

	def drawColumnNames(self):
		# Draw column names on listViewTab specified in config file
		# First, clear the container
		if len(self.columnNames.winfo_children()) > 0:
			for widget in self.columnNames.winfo_children():
				widget.destroy()

		f = ('Courier',12,'bold') # font for column names
		Label(self.columnNames,text="  ",width=2,font=f).grid(row=0,column=0,pady=5,padx=4) #edit button
		
		index = 1 # first column is blank for the edit button
		for i in self.listViewFields:
			Label(self.columnNames,text=str(i[0]),width=i[1],font=f).grid(row=0,column=index,pady=5,padx=5)
			index = index+1

	def drawNavFooter(self):
		# Add the navigation bar at the bottom of listViewTab
		f1 = ('Courier',15, "bold") # font
		f2 = ('Times',15, "bold") # font

		# create labels
		previousPage = Label(self.navFooter, text="\u21e6",font=f1) # unicode left arrow symbol
		nextPage = Label(self.navFooter, text="\u21e8",font=f1) # unicode right arrow symbol
		n = math.ceil(self.numRecords/self.recordsPerPage)
		self.currentPageLabel = Label(self.navFooter, text="Page "+str(self.pageNum+1)+" of "+str(n),font=f2,width=12,anchor="center")
		self.numRecordsLabel = Label(self.navFooter, text=str(self.numRecords)+" total records",font=f2)

		# Draw the labels
		previousPage.pack(side=LEFT)
		self.currentPageLabel.pack(side=LEFT)
		nextPage.pack(side=LEFT)
		self.numRecordsLabel.pack(side=RIGHT)
		
		# Bind events to the left and right arrow labels
		previousPage.bind("<Button-1>", self.previousPageCallback)
		nextPage.bind("<Button-1>", self.nextPageCallback)

	def previousPageCallback(self,event):
		if self.pageNum > 0:
			self.pageNum = self.pageNum - 1
			n = math.ceil(self.numRecords/self.recordsPerPage) # get num pages
			self.currentPageLabel['text'] = "Page "+str(self.pageNum+1)+" of "+str(n)
			self.populateDataList()
			self.dataList.canvas.yview_moveto(0) # scroll to top when page is changed

	def nextPageCallback(self,event):
		if (self.pageNum+1)*self.recordsPerPage < self.numRecords:
			self.pageNum = self.pageNum + 1
			n = math.ceil(self.numRecords/self.recordsPerPage) # get num pages
			self.currentPageLabel['text'] = "Page "+str(self.pageNum+1)+" of "+str(n)
			self.populateDataList()
			self.dataList.canvas.yview_moveto(0) # scroll to top when page is changed

	def drawRecordRows(self):
		f = ('Courier',12) # font for field data

		# Create a 2D array to store references to all record field Labels
		self.recordLabels = [[None for col in range(0,len(self.listViewFields)+1)] for row in range(0,self.recordsPerPage)]

		# Create empty Labels for every record row
		for row in range(0,self.recordsPerPage):
			# Draw the edit button Label
			self.recordLabels[row][0] = Label(self.dataList.interior,text="",width=0,font=f)
			img = PhotoImage(file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "editSymbol.gif"))
			self.recordLabels[row][0]['image'] = img # add edit button to column 0
			self.recordLabels[row][0].image = img
			self.recordLabels[row][0].grid(row=row,column=0,padx=5,sticky=E)

			# Draw an empty Label for each field
			for column, field in enumerate(self.listViewFields, start=1):
				self.recordLabels[row][column] = Label(self.dataList.interior,text="",width=field[1],font=f)
				self.recordLabels[row][column].grid(row=row,column=column,padx=5)
		
		# Boolean array to tell if row is displayed or not (using grid, grid_remove())
		self.rowsDisplayed = [True] * self.recordsPerPage

	def populateDataList(self):
		# populate empty labels
		for row in range(0,self.recordsPerPage): # num rows
			databaseIndex = self.pageNum * self.recordsPerPage + row
			if databaseIndex >= self.numRecords: # Clear the remaining rows on the last page
				self.rowsDisplayed[row] = False
				# Remove (but don't destroy) the labels for the fields in the row
				self.recordLabels[row][0].grid_remove() #edit button
				for column in range(0,len(self.listViewFields)):
					self.recordLabels[row][column+1].grid_remove() #fields
			else: # row is displayed
				if self.rowsDisplayed[row] == False: # if row was previously removed
					# Restore the labels for the fields in the row
					self.rowsDisplayed[row] = True
					self.recordLabels[row][0].grid(row=row,column=0) #edit button
					
					for column in range(0,len(self.listViewFields)):
						self.recordLabels[row][column+1].grid(row=row,column=column+1) #fields

				# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
				# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
				# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
				# TODO: Add event binding to edit button here!
				self.recordLabels[row][0].bind("<Button-1>", lambda event, arg=databaseIndex: self.editButtonCallback(event, arg))
				# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
				# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
				# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

				# Add data to each column for the record
				for col, field in enumerate(self.listViewFields): # num columns (fields)
					s = self.database[databaseIndex].fields[field[0]]
					if field[0] == "ID":
						s = str(s).zfill(5)
					else:
						s = str(s)
					# s = self.getRecordFieldData(databaseIndex, self.listViewFields[column][0]) #row=databaseIndex,column=field
					self.recordLabels[row][col+1]['text'] = s # 0th field is edit button

	def editButtonCallback(self, event, databaseIndex):
		print(databaseIndex) # this works
		self.notebook.select(self.dataEntryTab) #switch over to dataEntryTab

		####### After 2 seconds, switch back #######
		# self.master.update()
		# self.master.after(2000)
		# self.notebook.select(self.listViewTab)

	def createEasyDatabase(self):
		# Create a 2D array
		self.database = [None] * self.numRecords
		for i in range(0,self.numRecords):
			self.database[i] = SimpleRecord(i)
			self.database[i].fillWithFakeData()

# Fake database for GUI testing
# Database is an array of SimpleRecord entries
class SimpleRecord:
	def __init__(self,ID):
		# Dictionary of fields, initialize to empty 
		self.fields = {
			"ID":ID,
			"Name":"",
			"Qty":0,
			"X":0.0,
			"Y":0.0,
			"Date Created":"",
			"Last Modified":"",
			"Color":"",
			"Description":""
		}

	def fillWithFakeData(self):
		for key, value in self.fields.items():
			if key == "Name":
				self.fields[key] = "name_"+str(self.fields["ID"])
			elif key == "Qty":
				self.fields[key] = str(random.randint(0,27))
			elif key == "X":
				self.fields[key] = format(38.900070 + self.fields["ID"]*0.000001,'.6f')
			elif key == "Y":
				self.fields[key] = format(-77.049630+ self.fields["ID"]*0.000001,'.6f')
			elif key == "Date Created":
				self.fields[key] = time.strftime("%Y-%m-%d %H:%M")
			elif key == "Last Modified":
				self.fields[key] = time.strftime("%Y-%m-%d %H:%M")
			elif key == "Description":
				self.fields[key] = "This is a description for item with id "+str(self.fields["ID"])+"."



if __name__ == "__main__":
	root = Tk()
	a = GUI(root) # make an instance of GUI

	# Run a
	root.mainloop()