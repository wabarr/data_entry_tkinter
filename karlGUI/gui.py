# Karl Preisner
# 7 March 2018

""" 
Current version:
- check list controls dynamic visibility of fields
"""

from tkinter import *
from tkinter.ttk import *

NUM_FIELDS = 10

class GUI:
	def __init__(self, master):
		self.master = master

		# Set Window Title
		self.master.title("Fossile Data Entry")
		# Set Window Dimensions
		self.master.minsize(width = 600, height = 400)
		self.master.maxsize(width = 600, height = 400)

		# draw main page
		self.drawMainPage()

	# This method calls the other draw methods
	def drawMainPage(self):
		self.drawFieldToggleButtons()
		self.drawNoteBook()

	# Draw the notebook. This creates the two tabbed windows. 
	def drawNoteBook(self):
		# Create notebook (it is a frame that with multiple tabbed windows)
		self.notebook = Notebook(self.master)

		# vscrollbar
		self.vscrollbar = Scrollbar(self.master, orient = VERTICAL)

		# notebook tabs
		self.listViewTab = Canvas(self.notebook, yscrollcommand = self.vscrollbar.set)
		self.dataEntryTab = Frame(self.notebook)
		self.vscrollbar.config(command = self.listViewTab.yview) #assign vscrollbar to listViewTab
		
		self.vscrollbar.pack(side=RIGHT, fill=Y)

		self.notebook.add(self.listViewTab, text = "List View")
		self.notebook.add(self.dataEntryTab, text = "Data Entry")
		

		# draw everything
		self.notebook.pack(side=TOP,fill=BOTH,expand=True,ipadx=5,ipady=5)
		
		
		
		# # add a scroll bar to the listViewTab
		# self.scrollbar = Scrollbar(self.listViewTab)
		


		# self.listViewTab.config(yscrollcommand=self.scrollbar.set)
		# self.scrollbar.config(command=self.listViewTab.yview)

		for i in range(0,30):
			Label(self.listViewTab,text=str(i)).pack(side=TOP)

		
	# def exampleListViewItems(self):


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