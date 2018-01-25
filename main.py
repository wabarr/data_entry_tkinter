from Tkinter import *
import tkMessageBox
from models import Record, db
from peewee import IntegrityError
from config import Config


class DataEntry():

    def __init__(self, master):
        #initiate master title
        self.master = master
        self.master.title(config.options["project title"])
        Grid.columnconfigure(self.master, 0, weight=1)

        self.create_db_tables()
        self.create_list_page()
        self.populate_list_items()

    def create_list_page(self):

        self.itemsLabel = Frame(self.master)
        self.itemsLabel.grid(row=0, column=0)
        Grid.columnconfigure(self.itemsLabel, 0, weight=1)
        Label(self.itemsLabel, text="Items in database", font=("Arial", 20, 'bold')).grid(row=0,column=0)

        self.add_new = Frame(self.master)
        self.add_new.grid(row=1, column=0)
        Grid.columnconfigure(self.add_new, 0, weight=1)
        Grid.columnconfigure(self.add_new, 1, weight=1)
        Button(self.add_new, text="Add Record", command=self.add_record).grid(row=1, column=0)
        self.nameValue = StringVar()
        Entry(self.add_new, textvariable=self.nameValue).grid(row=1, column=2)

        self.headerrow = Frame(self.master, bg="gray92")
        self.headerrow.grid(row=2, column=0, sticky=N+S+E+W)
        for field in enumerate(Record._meta.sorted_field_names):
            Grid.columnconfigure(self.headerrow, field[0], weight=1)
            Label(self.headerrow, text=field[1]).grid(row=2, column=field[0])


        self.items = Frame(self.master, bg="gray92")
        for record in enumerate(Record._meta.sorted_field_names):
            Grid.columnconfigure(self.items, record[0], weight=1)
        self.items.grid(row=3, column=0, sticky=N+S+E+W)

    def create_db_tables(self):
        if Record.table_exists():
            tkMessageBox.showerror("Table exists", "The Record table already exists. You blast that db. ")
        else:
            db.create_tables([Record])

    def populate_list_items(self):
        for item in self.items.winfo_children():
            item.destroy()

        for record in enumerate(Record.select()):
            headerrows = 3
            for field in enumerate(Record._meta.sorted_field_names):
                theText = getattr(record[1], field[1])
                Label(self.items, text=theText).grid(row=record[0] + headerrows, column=field[0])
            #Button(self.items,text="Delete Record", command= lambda record=record : self.delete_record(theID=record[1].id)).grid(row=record[0] + headerrows, column=2, sticky=N+S+E+W, padx=1, pady=1)

    def add_record(self):
        try:
           Record.create(name=self.nameValue.get())
        except IntegrityError:
           tkMessageBox.showerror("Validation Error", "I can't create the record.  Please enter values for all fields.")
        self.nameValue.set("")
        self.populate_list_items()

    def delete_record(self, theID):
        theRecord = Record.get(Record.id == theID)
        theRecord.delete_instance()
        self.populate_list_items()

root = Tk()

config = Config()
config.validate()

root.geometry("1000x600")
my_gui = DataEntry(root)
root.mainloop()