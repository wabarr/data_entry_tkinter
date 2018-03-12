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
* optimize widget destroy for listViewTab
* arrow keys/scroll wheel for navigation
* column Configuration
* go to specific page in page navigation
* search bar
* edit record button
* Add dataEntry
	- update self.numRecords, self.numRecordsLabel upon save of entry
"""

class GUI:
	def __init__(self, master):
		self.master = master

		# Set Window Title
		self.master.title("Fossile Data Entry")
		# Set Window Dimensions
		# self.master.minsize(width = 600, height = 400)
		# self.master.maxsize(width = 600, height = 400)
		self.master.geometry('800x600')

		# GUI settings
		self.recordsPerPage = 10 # if more than 50 and rendering is SLOW

		# Class Variables
		self.pageNum = 0 # Which page of self.dataList are we looking at
		self.numRecords = 97

		self.getListViewFields()

		# draw main page
		self.drawMainPage()


	def getListViewFields(self):
		# Get all fields selected to be shown in listView

		# TODO: Retrieve from config file
		# field is a tuple: ("name", "type", number of characters to be displayed)
		self.listViewFields = [
			("ID","int",6),("Name","string",10),
			("Qty","int",6),("x","float",10),
			("y","float",10),("Date Created","string",16),
			("Last Modified","string",16)]

		self.listViewFields = [
			("ID","int",6),("Name","string",10),
			("Qty","int",6),("Date Created","string",16),
			("Last Modified","string",16),("Color","string",10),("ID","int",6)]

	def getFields(self):
		# Get all fields defined in config file.
		# All of these fields will be shown in dataEntryTab.
		pass

	# This method calls the other draw methods
	def drawMainPage(self):
		self.drawNoteBook()
		self.drawListViewTab()
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
		for widget in self.listViewTab.winfo_children():
			widget.destroy()

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

	def destroyListViewTab(self):
		for widget in frame.winfo_children():
			widget.destroy()

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
			Label(self.columnNames,text=str(i[0]),width=i[2],font=f).grid(row=0,column=index,pady=5,padx=5)
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
			self.recordLabels[row][0] = Label(self.dataList.interior,text="",width=2,font=f)
			self.recordLabels[row][0].grid(row=row,column=0,padx=5,sticky=E)

			# Draw an empty Label for each field
			for column, field in enumerate(self.listViewFields, start=1):
				self.recordLabels[row][column] = Label(self.dataList.interior,text="",width=field[2],font=f)
				self.recordLabels[row][column].grid(row=row,column=column,padx=5)
				

	def populateDataList(self):
		# populate empty labels

		# #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		# # this isn't correct
		img = PhotoImage(file="editSymbol.gif")
		# self.editButtons = [None]*self.recordsPerPage

		# # add edit image to Label and create binding
		# editButtons[row] = Label(self.dataList.interior,image=img,width=2,font=f)
		# editButtons[row].image = img # save the button's image from garbage collection 
		# editButtons[row].grid(row=row,column=0,padx=5,ipadx=0,sticky=E)
		# #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

		for row in range(0,self.recordsPerPage): # num rows
			ID = self.pageNum * self.recordsPerPage + row
			if ID > self.numRecords:
				# This is the last page of data and it is not full
				# Clear the remaining rows
				self.recordLabels[row][0]['image'] = None # clear edit button image
				self.recordLabels[row][0].image = None
				# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
				# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
				# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
				# TODO: Remove event binding to edit button!
				# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
				# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
				# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

				for column in range(0,len(self.listViewFields)):
					self.recordLabels[row][column+1]['text'] = "" # clear field labels
			else:
				self.recordLabels[row][0]['image'] = img # add edit button to column 0
				self.recordLabels[row][0].image = img
				# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
				# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
				# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
				# TODO: Add event binding to edit button here!
				# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
				# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
				# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

				# Add data to each column for the record
				for column in range(0,len(self.listViewFields)): # num columns (fields)
					s = self.getRecordFieldData(ID, self.listViewFields[column][0]) #row=ID,column=fieldName
					self.recordLabels[row][column+1]['text'] = s # 0th column is edit button

	def populateDataList_old(self):
		# First, clear the container
		if len(self.dataList.interior.winfo_children()) > 0:
			for widget in self.dataList.interior.winfo_children():
				widget.destroy()

		f = ('Courier',12) # font for field data
		img = PhotoImage(file="editSymbol.gif")

		# populate dataList with some stuff
		# Note: To add a widget to self.dataList, you need to use 'self.dataList.interior'
		m = self.pageNum*self.recordsPerPage
		n = m+self.recordsPerPage
		if self.numRecords < n:
			n = self.numRecords
		for i in range(m,n):
			# Edit button
			editButton = Label(self.dataList.interior,image=img,width=2,font=f)
			editButton.image = img # save the button's image from garbage collection 
			editButton.grid(row=i,column=0,padx=5,ipadx=0,sticky=E)

			# Rest of the fields as defined in config file
			index = 1 # first column is the edit button
			for col in self.listViewFields:
				# Get field data from database for record i
				s = self.getRecordFieldData(i,col[0])
				# Make the label and draw it
				Label(self.dataList.interior,text=s,width=col[2],font=f).grid(row=i,column=index,padx=5)
				index = index+1 #increment column index to get next field


	def getRecordFieldData(self, row, fieldName):
		# returns a string
		if fieldName == "ID":
			return str(row).zfill(5)
		elif fieldName == "Name":
			return "name_"+str(row)
		elif fieldName == "Qty":
			return str(random.randint(0,50))
		elif fieldName == "x":
			return format(38.900070 + row*0.000001,'.6f')
		elif fieldName == "y":
			return format(-77.049630+ row*0.000001,'.6f')
		elif fieldName == "Date Created":
			return time.strftime("%Y-%m-%d %H:%M")
		elif fieldName == "Last Modified":
			return time.strftime("%Y-%m-%d %H:%M")
		else:
			return "N/A"


if __name__ == "__main__":
	root = Tk()
	a = GUI(root) # make an instance of GUI

	# Run a
	root.mainloop()