from Tkinter import *
import tkMessageBox
from models import Record, db
import yaml

with open("config.yml", "r") as configfile:
    config = yaml.load(configfile)
    configfile.close()

class DataEntry:

    def __init__(self, master):
        self.master = master
        self.master.title(config["project title"])
        Grid.columnconfigure(self.master, 0, weight=1)

        if not Record.table_exists():
            db.create_tables([Record])

        self.buttons = Frame(master)
        self.buttons.grid(row=0, column=0)
        Grid.columnconfigure(self.buttons, 0, weight=1)
        Button(self.buttons, text="Add Record", command=self.add_record).grid(row=1, column=0)
        Button(self.buttons, text="Close", command=master.quit).grid(row=1, column=1)

        self.itemsLabel = Frame(master)
        self.itemsLabel.grid(row=1, column=0)
        Grid.columnconfigure(self.itemsLabel, 0, weight=1)
        Label(self.itemsLabel, text="Items in database", font=("Arial", 20, 'bold')).grid(row=0,column=0)


        self.items = Frame(master)
        Grid.columnconfigure(self.items, 0, weight=1)
        Grid.columnconfigure(self.items, 1, weight=4)
        Grid.columnconfigure(self.items, 2, weight=1)
        self.items.grid(row=2, column=0, sticky=N+S+E+W)
        self.populate_items()

    def populate_items(self):
        for item in self.items.winfo_children():
            #if item.widgetName == "Button":
            item.destroy()

        for record in enumerate(Record.select()):
            Label(self.items, text=record[1].id).grid(row=record[0] + 2, column=0, sticky=N+S+E+W)
            Label(self.items, text=record[1].name).grid(row=record[0] + 2, column=1, sticky=N+S+E+W)
            Button(self.items,text="Delete Record", command= lambda record=record : self.delete_record(theID=record[1].id)).grid(row=record[0] + 2, column=2, sticky=N+S+E+W)

    def add_record(self):
        Record.create(name="new_record")
        self.populate_items()

    def delete_record(self, theID):
        theRecord = Record.get(Record.id == theID)
        theRecord.delete_instance()
        self.populate_items()

root = Tk()
root.geometry("1000x600")
my_gui = DataEntry(root)
root.mainloop()