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
# import ImageTk

# other stuff
import time, random

# Important development tips:
#   - To add a widget to a VerticalScrolledFrame v, you must use 'v.interior'
#     Example: Label(self.v.interior, text="hello")


"""
TODO:
* optimize widget destroy for listViewTab
* arrow keys for navigation
* highlight an entry row
* double click entry row to visit data Entry tab
* data entry tab
* column Configuration
"""

NUM_FIELDS = 10
NUM_DATA = 4000

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
		self.dataPerPage = 50

		# Class Variables
		self.pageNum = 0 # Which page of self.dataList are we looking at

		# draw main page
		self.drawMainPage()

	# This method calls the other draw methods
	def drawMainPage(self):
		self.drawFieldToggleButtons()
		self.drawNoteBook()
		self.drawListViewTab()
		self.populateListViewTab()

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

		# Create the frames in the list view tab
		self.columnNames = Frame(self.listViewTab)
		self.dataList = VerticalScrolledFrame(self.listViewTab)
		self.navFooter = Frame(self.listViewTab)
		# draw them
		self.columnNames.pack(fill=X)
		Separator(self.listViewTab, orient="horizontal").pack(fill=X) # separator line
		self.dataList.pack(fill=BOTH,expand=True)
		Separator(self.listViewTab, orient="horizontal").pack(fill=X) # separator line
		self.navFooter.pack(fill=X)

	def destroyListViewTab(self):
		for widget in frame.winfo_children():
			widget.destroy()

	def populateListViewTab(self):
		# Note on font sizes
		# - columnName font/padx line up perfectly with field data columns only with the current settings
		f1 = ('Courier',12,'bold') # font for column names
		f2 = ('Courier',12) # font for field data
		# Add column names to top
		# Label(self.columnNames,text="ID",  width=6, font=f1).grid(row=0,column=0,pady=5,padx=3)
		# Label(self.columnNames,text="Name",width=10,font=f1).grid(row=0,column=1,pady=5,padx=3)
		# Label(self.columnNames,text="Qty", width=6, font=f1).grid(row=0,column=2,pady=5,padx=3)
		# Label(self.columnNames,text="x",   width=10,font=f1).grid(row=0,column=3,pady=5,padx=3)
		# Label(self.columnNames,text="y",   width=10,font=f1).grid(row=0,column=4,pady=5,padx=3)
		# Label(self.columnNames,text="Date",width=16,font=f1).grid(row=0,column=5,pady=5,padx=3)
		# Label(self.columnNames,text="Last modified",width=16,font=f1).grid(row=0,column=6,pady=5,padx=3)
		# Label(self.columnNames,text="Image",width=16,font=f1).grid(row=0,column=7,pady=5,padx=3)

		# label version
		Label(self.columnNames,text="  ",width=2,font=f1).grid(row=0,column=0,pady=5,padx=5) #edit button
		Label(self.columnNames,text="ID",  width=6, font=f1).grid(row=0,column=1,pady=5,padx=5)
		Label(self.columnNames,text="Name",width=10,font=f1).grid(row=0,column=2,pady=5,padx=5)
		Label(self.columnNames,text="Qty", width=6, font=f1).grid(row=0,column=3,pady=5,padx=5)
		Label(self.columnNames,text="x",   width=10,font=f1).grid(row=0,column=4,pady=5,padx=5)
		Label(self.columnNames,text="y",   width=10,font=f1).grid(row=0,column=5,pady=5,padx=5)
		Label(self.columnNames,text="Date created", width=16,font=f1).grid(row=0,column=6,pady=5,padx=5)
		Label(self.columnNames,text="Last modified",width=16,font=f1).grid(row=0,column=7,pady=5,padx=5)


		# populate dataList with some stuff
		# Note: To add a widget to self.dataList, you need to use 'self.dataList.interior'

		f = ('Courier',12) # font
		m = self.pageNum*self.dataPerPage
		n = m+self.dataPerPage
		if NUM_DATA < n:
			n = NUM_DATA
		for i in range(m,n):
			# Edit button
			# pick a (small) image file you have in the working directory ...
			img = PhotoImage(file="editSymbol2.gif")
			# create the image button, image is above (top) the optional text
			editButton = Label(self.dataList.interior,font=f,image=img,width=2,borderwidth=0,relief=RAISED)
			# save the button's image from garbage collection (needed?)
			editButton.image = img

			# create the fields
			ID =   Label(self.dataList.interior,font=f2,width=6)
			name = Label(self.dataList.interior,font=f2,width=10)
			qty =  Label(self.dataList.interior,font=f2,width=6)
			x =    Label(self.dataList.interior,font=f2,width=10)
			y =    Label(self.dataList.interior,font=f2,width=10)
			date = Label(self.dataList.interior,font=f2,width=16)
			modified = Label(self.dataList.interior,font=f2,width=16)

			# draw the fields
			editButton.grid(row=i,column=0,padx=5,ipadx=3,sticky=E)
			ID.grid(row=i,  column=1,padx=5)
			name.grid(row=i,column=2,padx=5)
			qty.grid(row=i, column=3,padx=5)
			x.grid(row=i,   column=4,padx=5)
			y.grid(row=i,   column=5,padx=5)
			date.grid(row=i,column=6,padx=5)
			modified.grid(row=i,column=7,padx=5)

			# Fill the fields with some junk
			ID['text']=str(i).zfill(5)
			name['text']="name_"+str(i)
			qty['text']=str(random.randint(0,50))
			x['text']=format(38.900070 + i*0.000001,'.6f')
			y['text']=format(-77.049630+ i*0.000001,'.6f')
			date['text']=time.strftime("%Y-%m-%d %H:%M")
			modified['text']=time.strftime("%Y-%m-%d %H:%M")

		# Add the navigation bar at the bottom
		f1 = ('Courier',15, "bold") # font
		f2 = ('Times',15) # font
		previousPage = Label(self.navFooter, text="\u21e6",font=f1)
		nextPage = Label(self.navFooter, text="\u21e8",font=f1)
		# Pack them in
		previousPage.pack(side=LEFT)
		n = int(NUM_DATA/self.dataPerPage)
		Label(self.navFooter, text="Page "+str(self.pageNum+1)+" of "+str(n),font=f2).pack(side=LEFT)
		nextPage.pack(side=LEFT)
		Label(self.navFooter, text=str(NUM_DATA)+" total records",font=f2).pack(side=RIGHT)
		previousPage.bind("<Button-1>", self.previousPageCallback)
		nextPage.bind("<Button-1>", self.nextPageCallback)

	def previousPageCallback(self,event):
		if self.pageNum > 0:
			self.pageNum = self.pageNum - 1
			self.drawListViewTab()
			self.populateListViewTab()

	def nextPageCallback(self,event):
		if (self.pageNum+1)*self.dataPerPage < NUM_DATA:
			self.pageNum = self.pageNum + 1
			self.drawListViewTab()
			self.populateListViewTab()









	# This method will be replaced by the config file.
	def drawFieldToggleButtons(self):
		self.showField = [None] * NUM_FIELDS #variables to know if fieldToggle is on/off
		self.fieldToggle = [None] * NUM_FIELDS # list of checkbuttons to toggle fields on/off
		for i in range(0,NUM_FIELDS): # initialize array elements
			self.showField[i] = BooleanVar()
			self.showField[i].set(True)

		# create a frame for the fieldToggle checkbuttons to sit inside of
		self.group = LabelFrame(self.master, text="Configuration options (this will be removed after config file is built)")
		self.group.pack(side=TOP,fill=X,padx=5,pady=5,ipadx=5,ipady=5)

		# initialize toggle field checkbuttons
		self.fieldToggle[0] = Checkbutton(self.group, text="field 0", variable=self.showField[0], command=lambda: self.displayField_callback(0))
		self.fieldToggle[1] = Checkbutton(self.group, text="field 1", variable=self.showField[1], command=lambda: self.displayField_callback(1))
		self.fieldToggle[2] = Checkbutton(self.group, text="field 2", variable=self.showField[2], command=lambda: self.displayField_callback(2))
		self.fieldToggle[3] = Checkbutton(self.group, text="field 3", variable=self.showField[3], command=lambda: self.displayField_callback(3))

		# draw toggle fields to the screen (inside of group)
		self.fieldToggle[0].pack(side=LEFT, padx=5)
		self.fieldToggle[1].pack(side=LEFT, padx=5)
		self.fieldToggle[2].pack(side=LEFT, padx=5)
		self.fieldToggle[3].pack(side=LEFT, padx=5)

	# This method will read the config file and be called when building the pages.
	def displayField_callback(self, field_num):
		# turn on/off field based on checkbutton field toggle
		if self.showField[field_num].get(): # True/False
			# print("field",field_num,"on")
			pass
		else:
			# print("field",field_num,"off")
			pass


if __name__ == "__main__":
	root = Tk()
	a = GUI(root) # make an instance of GUI

	# Run a
	root.mainloop()