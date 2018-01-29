from tkinter import *
from tkinter import messagebox
import math
from models import Record, db
import peewee
from peewee_validates import ModelValidator
from config import Config
import os
from tkinter.ttk import Separator

class DataEntry():

    def __init__(self, master):
        #initiate master title
        self.master = master
        self.master.title(config.options["project title"])
        self.records_per_page = config.options["records_per_page"]
        self.fieldnames = []
        for fieldname in Record._meta.sorted_field_names:
            if not fieldname == "id":
                self.fieldnames.append(fieldname)

        self.create_db_tables()
        self.draw_list_page()
        self.populate_list_items()
        self.draw_footer()


    def draw_list_page(self):

        # self.itemsLabel = Frame(self.master)
        # self.itemsLabel.grid(row=0, column=0)
        # Grid.columnconfigure(self.itemsLabel, 0, weight=1)
        # Label(self.itemsLabel, text="Items in database", font=("Arial", 20, 'bold')).grid(row=0,column=0)

        # self.add_new = Frame(self.master)
        # self.add_new.grid(row=1, column=0)
        # Grid.columnconfigure(self.add_new, 0, weight=1)
        # Grid.columnconfigure(self.add_new, 1, weight=1)
        # Button(self.add_new, text="Add Record", command=self.add_record).grid(row=1, column=0)
        # self.nameValue = StringVar()
        # Entry(self.add_new, textvariable=self.nameValue).grid(row=1, column=2)

        self.search_bar=Frame(self.master)
        self.search_bar.grid(row=0, column=0, sticky=N+S+E+W)
        searchquery = StringVar()
        #searchquery.set("")
        def callback(*args):
            ## currently works, but assumes that fieldnames pertain only to
            ## text fields
            querystring=searchquery.get()
            fieldnames = ["name", "photo"]
            modelname = "Record"
            wherestring = "%%%s%%" % (querystring,)
            clauses = []
            for fieldname in fieldnames:
                clauses.append("%s.%s ** '%s'" % (modelname, fieldname, wherestring))
            fullquery = " | ".join(clauses)
            rs = Record.select().where(eval(fullquery))
            self.populate_list_items(query=rs)
        searchbox = Entry(self.search_bar, textvariable=searchquery)
        searchbox.grid(row=0,column=0, sticky=N+S+E+W)
        #searchbutton = Button(self.search_bar, text="Search")
        #searchbutton.grid(row=0, column=1, sticky=N+S+E+W)
        #searchbutton.bind("<Button 1>", callback)
        searchquery.trace("w", callback)



        #make the items frame
        self.items = Frame(self.master, bg="white")
        self.items.grid(row=1, column=0, sticky=N+S+E+W)

    def setup_items_frame(self):
        #self.headerrows = 3  # how many total headerrorws are there in the items frame?
        #header row
        for field in enumerate(self.fieldnames):
            Grid.columnconfigure(self.items, field[0], weight=1)
            cell = Label(self.items,  text=field[1], font=("Arial", 14, "bold"))
            cell.grid(row=2, column=field[0])
            #cell.insert(0,field[1])
            #cell.config(justify="center", state="readonly",)


        #row for delete icon
        Grid.columnconfigure(self.items, len(self.fieldnames), weight=1)

        for record in enumerate(self.fieldnames):
            Grid.columnconfigure(self.items, record[0], weight=1)

    def draw_detail_page(self, pk):
        #draw the detail page for a particular instance of the Record class given by pk
        pass

    def do_query(self):
        pass

    def create_db_tables(self):
        if Record.table_exists():
            messagebox.showerror("Table exists", "The Record table already exists. You blast that db. ")
        else:
            db.create_tables([Record])

    def populate_list_items(self, query = Record.select(), orderfield=Record.id):
        for item in self.items.winfo_children():
            item.destroy()
        self.setup_items_frame()

        #dir_path = os.path.dirname(os.path.realpath(__file__))
        #trashcan = PhotoImage(file=os.path.join(dir_path, "assets/icons/trashcan.gif"))
        for record in enumerate(query.order_by(orderfield).limit(self.records_per_page)):

            for field in enumerate(self.fieldnames):
                theText = getattr(record[1], field[1])
                if not theText:
                    theText = '-'
                cell = Entry(self.items)
                cell.grid(row=record[0] + 4, column=field[0])
                cell.insert(0, theText)
                cell.config(justify="center", state="readonly", font=("Arial", 12))
            #delete = Label(self.items, image=trashcan)
            #delete.image = trashcan
            delete = Label(self.items, text="-")
            delete.bind("<Button-1>",lambda e, record=record : self.delete_record(theID=record[1].id))
            delete.grid(row=record[0] + 4, column=len(self.fieldnames), sticky=N+S+E+W, padx=1, pady=1)
        self.draw_data_entry_form()
        #self.draw_nrow_selector()

    def draw_data_entry_form(self):
       #self.items.grid(row=1 + self.records_per_page + 3, column=0)

       self.entry_form_values = {}
       for field in enumerate(self.fieldnames):
           self.entry_form_values.update({field[1]:StringVar()})
           cell = Entry(self.items, textvariable=self.entry_form_values[field[1]])
           cell.grid(row=self.records_per_page+2, column=field[0], padx=1, pady=1)
           cell.config(font=("Arial", 12))
       add = Label(self.items, text="+")
       add.bind("<Button-1>", lambda e: self.add_record())
       add.grid(row=self.records_per_page+2, sticky=N+S+E+W, column=len(self.fieldnames))
       Separator(self.items, orient=HORIZONTAL).grid(row=999, columnspan=len(self.fieldnames), sticky="ew", pady=4)


    def add_record(self):

        new_record = Record()
        for field in self.fieldnames:
           if self.entry_form_values[field].get():
             setattr(new_record, field, self.entry_form_values[field].get())
        validator = ModelValidator(new_record)
        if validator.validate():
           new_record.save()
           self.populate_list_items()
           self.draw_footer()
        else:
           errorlist = []
           for key, value in validator.errors.items():
             errorlist.append("Error in field '%s': %s" %(key, value))
           messagebox.showerror("Invalid Data", "\n".join(errorlist))

    def delete_record(self, theID):
        theRecord = Record.get(Record.id == theID)
        if messagebox.askokcancel("Delete this record?", "Do you really want to delete record ID = %s?" %(theID)):
            theRecord.delete_instance()
            self.populate_list_items()
            self.draw_footer()

    # def draw_nrow_selector(self):
    #
    #     def set_records_per_page(n):
    #         self.records_per_page = n
    #         self.populate_list_items()
    #         self.draw_footer()
    #
    #     Label(self.items, text="Display Records").grid(row=1000, column=0)
    #     self.nRows = StringVar()
    #     self.nrows = "10"
    #     self.nRows.trace("w", lambda a, b, c: set_records_per_page(int(self.nRows.get())))
    #     # combobox = Combobox(self.items, textvariable=self.nRows)
    #     # combobox.config(justify="center")
    #     # combobox["values"] = ("10", "20", "30", "40", "50")
    #     # combobox.grid(row=1001, column=0)
    #     #combobox.set("10")

    def draw_footer(self):
        totalRecords = Record.select().count()
        totalPages = math.ceil(totalRecords/self.records_per_page)
        self.footer = Frame(self.master)
        self.footer.grid(row=1001, column=0)
        Label(self.footer, text="Showing %d of %d records" %(self.records_per_page,totalRecords,)).grid(row=0, column=0)
        Label(self.footer, text="<").grid(row=0, column=1)
        Label(self.footer, text="page %d of %d" % (1, totalPages)).grid(row=0, column=2)
        Label(self.footer, text=">").grid(row=0, column=3)





root = Tk()


config = Config()
config.validate()

root.geometry("%sx%s" %(root.winfo_screenwidth(), root.winfo_screenheight()))
my_gui = DataEntry(root)
root.mainloop()