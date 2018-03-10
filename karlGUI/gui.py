# Karl Preisner
# 7 March 2018

""" 
Current version:
- check list controls dynamic visibility of fields
"""

from tkinter import *
import tkinter as tk
from tkinter.ttk import *
from VerticalScrolledFrame import *

# Important development tips:
#   - To add a widget to a VerticalScrolledFrame v, you must use 'v.interior'
#     Example: Label(self.v.interior, text="hello")

NUM_FIELDS = 10

class GUI:
	def __init__(self, master):
		self.master = master

		# Set Window Title
		self.master.title("Fossile Data Entry")
		# Set Window Dimensions
		# self.master.minsize(width = 600, height = 400)
		# self.master.maxsize(width = 600, height = 400)

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

		Label(self.dataEntryTab,text="heyy, this is where your data enters me ;)").pack()
		Label(self.dataEntryTab,text="\nok.\nyou know what..\nthat was a sexaul joke.\nAnd you know what else?\nIt wasn't even that good.\nsorry.").pack()

	def drawListViewTab(self):
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

	def populateListViewTab(self):
		f = ('Courier',13,'bold') # font
		# Add column names
		Label(self.columnNames,text="ID  ",width=6,font=f).grid(row=0,column=0,pady=5,padx=0)
		Label(self.columnNames,text="Name",width=10,font=f).grid(row=0,column=1,pady=5,padx=0)
		Label(self.columnNames,text="x   ",width=10,font=f).grid(row=0,column=2,pady=5,padx=0)
		Label(self.columnNames,text="y   ",width=10,font=f).grid(row=0,column=3,pady=5,padx=0)

		# populate dataList with some stuff
		# Note: To add a widget to self.dataList, you need to use 'self.dataList.interior'
		f1 = ('Courier',12) # font
		f2 = ('Courier',12) # font
		for i in range(1,51):
			Label(self.dataList.interior,font=f1,width=6,text=str(i).zfill(5)).grid(row=i,column=0)
			name = Entry(self.dataList.interior,font=f2,width=10)
			x = Entry(self.dataList.interior,font=f1,width=10)
			y = Entry(self.dataList.interior,font=f1,width=10)
			name.grid(row=i,column=1)
			x.grid(row=i,column=2)
			y.grid(row=i,column=3)
			# Fill the entry boxes with some junk
			name.insert(0,"name_"+str(i))
			x.insert(0,format(38.900070 + i*0.000001,'.6f'))
			y.insert(0,format(-77.049630+ i*0.000001,'.6f'))

		f1 = ('Courier',15, "bold") # font
		f2 = ('Times',15) # font
		# Add the navigation bar at the bottom
		previousPage = Label(self.navFooter, text="\u21e6",font=f1)
		nextPage = Label(self.navFooter, text="\u21e8",font=f1)

		# previousPage.grid(row=0, column=0)
		# Label(self.navFooter, text="Page # of ###",font=f2).grid(row=0, column=1)
		# nextPage.grid(row=0, column=2)
		# Label(self.navFooter, text="#### total records",font=f2,anchor=E).grid(row=0, column=3,sticky=E)

		# try packing them in
		previousPage.pack(side=LEFT)
		Label(self.navFooter, text="Page # of ###",font=f2).pack(side=LEFT)
		nextPage.pack(side=LEFT)
		Label(self.navFooter, text="#### total records",font=f2).pack(side=RIGHT)

		def previous_page(*args):
			# TODO
			pass
		def next_page(*args):
			# TODO
			pass
		previousPage.bind("<Button-1>", previous_page)
		nextPage.bind("<Button-1>", next_page)

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