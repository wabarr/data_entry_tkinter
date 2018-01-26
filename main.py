from Tkinter import *
import tkMessageBox
from models import Record, db
from peewee import IntegrityError
from config import Config
import os


class DataEntry():

    def __init__(self, master):
        #initiate master title
        self.master = master
        self.master.title(config.options["project title"])
        Grid.columnconfigure(self.master, 0, weight=1)

        self.fieldnames = []
        for fieldname in Record._meta.sorted_field_names:
            if not fieldname == "id":
                self.fieldnames.append(fieldname)
        self.records_per_page = config.options["records_per_page"]

        self.create_db_tables()
        self.draw_list_page()
        self.populate_list_items()

    def draw_list_page(self):

        self.itemsLabel = Frame(self.master)
        self.itemsLabel.grid(row=0, column=0)
        Grid.columnconfigure(self.itemsLabel, 0, weight=1)
        Label(self.itemsLabel, text="Items in database", font=("Arial", 20, 'bold')).grid(row=0,column=0)

        # self.add_new = Frame(self.master)
        # self.add_new.grid(row=1, column=0)
        # Grid.columnconfigure(self.add_new, 0, weight=1)
        # Grid.columnconfigure(self.add_new, 1, weight=1)
        # Button(self.add_new, text="Add Record", command=self.add_record).grid(row=1, column=0)
        # self.nameValue = StringVar()
        # Entry(self.add_new, textvariable=self.nameValue).grid(row=1, column=2)


        #make the items frame
        self.items = Frame(self.master, bg="white")
        self.items.grid(row=3, column=0, sticky=N+S+E+W)

    def setup_items_frame(self):
        self.headerrows = 3  # how many total headerrorws are there in the items frame?
        #header row
        for field in enumerate(self.fieldnames):
            Grid.columnconfigure(self.items, field[0], weight=1)
            Label(self.items, text=field[1], font=("Arial", 14, 'bold')).grid(row=2, column=field[0])


        #row for delete icon
        Grid.columnconfigure(self.items, len(self.fieldnames), weight=0)

        for record in enumerate(self.fieldnames):
            Grid.columnconfigure(self.items, record[0], weight=1)

    def draw_detail_page(self, pk):
        #draw the detail page for a particular instance of the Record class given by pk
        pass

    def create_db_tables(self):
        if Record.table_exists():
            tkMessageBox.showerror("Table exists", "The Record table already exists. You blast that db. ")
        else:
            db.create_tables([Record])

    def populate_list_items(self):
        for item in self.items.winfo_children():
            item.destroy()
        self.setup_items_frame()

        dir_path = os.path.dirname(os.path.realpath(__file__))
        trashcan = PhotoImage(file=os.path.join(dir_path, "assets/icons/trashcan.gif"))

        for record in enumerate(Record.select().limit(self.records_per_page)):

            for field in enumerate(self.fieldnames):
                theText = getattr(record[1], field[1])
                if not theText:
                    theText = 'NA'
                Label(self.items, text=theText, wraplength=100, font=("Arial", 12 ), padx=10, pady=2).grid(
                    row=record[0] + self.headerrows, column=field[0])
            delete = Label(self.items, image=trashcan)
            delete.image = trashcan
            delete.bind("<Button-1>",lambda e, record=record : self.delete_record(theID=record[1].id))
            delete.grid(row=record[0] + self.headerrows, column=len(self.fieldnames), sticky=N+S+E+W, padx=3, pady=1)
        self.draw_data_entry_form()

    def draw_data_entry_form(self):
       #self.items.grid(row=self.headerrows + self.records_per_page + 1, column=0)

       self.entry_form_values = {}
       for field in enumerate(self.fieldnames):
           self.entry_form_values.update({field[1]:StringVar()})
           Entry(self.items, textvariable=self.entry_form_values[field[1]]).\
               grid(row=self.headerrows+self.records_per_page+1, column=field[0], padx=1, pady=2)
       add = Label(self.items, text="+")
       add.bind("<Button-1>", lambda e: self.add_record())
       add.grid(row=self.headerrows+self.records_per_page+1, column=len(self.fieldnames))

    def add_record(self):
        try:
           new_record = Record()
           for field in self.fieldnames:
              if self.entry_form_values[field].get():
                setattr(new_record, field, self.entry_form_values[field].get())
           new_record.save()
        except IntegrityError as e:
           tkMessageBox.showerror(e.strerror)
        #need to validate datatypes in data entry!
        self.populate_list_items()

    def delete_record(self, theID):
        theRecord = Record.get(Record.id == theID)
        if tkMessageBox.askokcancel("Delete this record?", "Do you really want to delete record ID = %s?" %(theID)):
            theRecord.delete_instance()
            self.populate_list_items()


root = Tk()

config = Config()
config.validate()

root.geometry("%sx%s" %(root.winfo_screenwidth(), root.winfo_screenheight()))
my_gui = DataEntry(root)
root.mainloop()