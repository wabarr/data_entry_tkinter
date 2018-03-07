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

	def drawMainPage(self):
		self.drawFieldToggleButtons()
		self.drawListView()

	def drawListView(self):
		# create a frame for the listView to sit inside of
		self.group2 = Frame(self.master)
		self.group2.pack(side=TOP,fill=BOTH,expand=True,ipadx=5,ipady=5)


		# Create notebook (this allows for multiple tabbed windows)
		self.notebook = Notebook(self.group2)

		tab1 = Frame(self.notebook)
		tab2 = Frame(self.notebook)
		tab3 = Frame(self.notebook)
		Label(tab1, text='Exit').pack(padx=20, pady=20)

		self.notebook.add(tab1, text = "List View",compound=TOP)
		self.notebook.add(tab2, text = "Data Entry")
		self.notebook.pack(side=TOP,fill=BOTH,expand=True)

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