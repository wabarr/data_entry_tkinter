from tkinter import *
from tkinter import messagebox
import math
from models import Record, db
import peewee
from peewee_validates import ModelValidator
from config import Config
import os
from tkinter.ttk import Separator, Notebook
from datetime import datetime

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

        self.tab1 = Frame(Notebook)
        self.tab2 = Frame(Notebook)
        Notebook.add(self.tab1, text="list view")
        Notebook.add(self.tab2, text="data entry")
        Notebook.grid(row=0, column=0)

        self.create_db_tables()
        self.draw_list_page()
        self.populate_list_items()
        self.draw_footer()
        self.draw_data_entry_form()


    def draw_list_page(self):

        self.search_bar=Frame(self.tab1)
        self.search_bar.grid(row=0, column=0, sticky=N+S+E+W)
        searchquery = StringVar()

        def search(*args):
            self.update_recordset(querystring=searchquery.get())

        def getready4query(*args):
            searchbox.delete(0, END)
            searchbox.config(foreground="black")

        searchbox = Entry(self.search_bar, textvariable=searchquery, foreground="grey")
        searchbox.grid(row=0,column=1, sticky=N+S+E+W)
        searchbox.bind("<Return>", search)
        searchbox.insert(0, "Search")
        searchbox.bind("<FocusIn>", getready4query)

        searchbutton = Button(self.search_bar, text="Search")
        searchbutton.grid(row=0, column=3, sticky=N+S+E+W)
        searchbutton.bind("<Button 1>", search)


        def clearcallback(*args):
            self.populate_list_items()
            searchbox.delete(0, END)
            searchbox.config(foreground="grey")
            searchbox.insert(0, "Search")
            clearbutton.focus_set()

        clearbutton = Button(self.search_bar, text="Clear")
        clearbutton.grid(row=0, column=4, sticky=N + S + E + W)
        clearbutton.bind("<Button 1>", clearcallback)


        #make the items frame
        self.items = Frame(self.tab1, bg="white")
        self.items.grid(row=1, column=0, sticky=N+S+E+W)

    def setup_items_frame(self):
        self.make_header_row(self.items)
        #row for delete icon
        Grid.columnconfigure(self.items, len(self.fieldnames), weight=1)

        for record in enumerate(self.fieldnames):
            Grid.columnconfigure(self.items, record[0], weight=1)

    def draw_detail_page(self, pk):
        #draw the detail page for a particular instance of the Record class given by pk
        pass

    def update_recordset(self, querystring, modelname="Record"):
        if querystring == "":
            self.populate_list_items()
        else:
            fieldnames = ["name", "photo"]
            wherestring = "%%%s%%" % (querystring,)
            clauses = []
            for fieldname in fieldnames:
                clauses.append("%s.%s ** '%s'" % (modelname, fieldname, wherestring))
            fullquery = " | ".join(clauses)
            rs = Record.select().where(eval(fullquery))
            self.populate_list_items(query=rs)

    def create_db_tables(self):
        if Record.table_exists():
            messagebox.showerror("Table exists", "The Record table already exists. You blast that db. ")
        else:
            db.create_tables([Record])

    def populate_list_items(self, query = Record.select(), orderfield=Record.id, currentpage=1):
        for item in self.items.winfo_children():
            item.destroy()
        self.setup_items_frame()

        if currentpage == 0:
            self.currentpage = 1
        else:
            self.currentpage = currentpage #for paginated search results

        def format_time(input):
            try:
                return(datetime.strftime(input, "%Y-%m-%d %H:%M:%S"))
            except TypeError:
                return(input)

        for record in enumerate(query.order_by(orderfield).limit(self.records_per_page).paginate(self.currentpage, self.records_per_page)):

            for field in enumerate(self.fieldnames):
                theText = getattr(record[1], field[1])
                if not theText:
                    theText = '-'
                cell = Entry(self.items)
                cell.grid(row=record[0] + 4, column=field[0])
                cell.insert(0, format_time(theText))
                cell.config(justify="center", state="readonly", font=("Arial", 12))

            delete = Label(self.items, text="-")
            delete.bind("<Button-1>",lambda e, record=record : self.delete_record(theID=record[1].id))
            delete.grid(row=record[0] + 4, column=len(self.fieldnames), sticky=N+S+E+W, padx=1, pady=1)
        Separator(self.items, orient=HORIZONTAL).grid(row=999, columnspan=len(self.fieldnames), sticky="ew", pady=4)
        self.draw_footer(query=query)

    def make_header_row(self, frame, row=2):
        for field in enumerate(self.fieldnames):
            Grid.columnconfigure(frame, field[0], weight=1)
            cell = Label(frame,  text=field[1], font=("Arial", 14, "bold"))
            cell.grid(row=row, column=field[0])

    def draw_data_entry_form(self):
       self.make_header_row(self.tab2, row=0)
       self.entry_form_values = {}
       for field in enumerate(self.fieldnames):
           self.entry_form_values.update({field[1]:StringVar()})
           cell = Entry(self.tab2, textvariable=self.entry_form_values[field[1]])
           cell.grid(row=1, column=field[0], padx=1, pady=1)
           cell.config(font=("Arial", 12))
       add = Label(self.tab2, text="+")
       add.bind("<Button-1>", lambda e: self.add_record())
       add.grid(row=1, sticky=N+S+E+W, column=len(self.fieldnames))



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

    def draw_footer(self, query=Record.select()):
        totalRecords = Record.select().count()
        queriedRecords = query.count()
        totalPages = math.ceil(queriedRecords/self.records_per_page)
        try:
            for item in self.footer.winfo_children():
                item.destroy()
        except AttributeError:
            self.footer = Frame(self.tab1)
            self.footer.grid(row=1001, column=0)
        if totalRecords == queriedRecords:
            Label(self.footer, text="%d total records" %(totalRecords,)).grid(row=0, column=0)
        else:
            Label(self.footer, text="Showing %d matching records (of %d total records)" % (queriedRecords, totalRecords,)).grid(row=0, column=0)
        previouspage = Label(self.footer, text="<")
        previouspage.grid(row=0, column=1)
        Label(self.footer, text="page %d of %d" % (self.currentpage, totalPages)).grid(row=0, column=2)
        nextpage = Label(self.footer, text=">")
        nextpage.grid(row=0, column=3)

        def previous_page(*args):
            self.populate_list_items(query=query, currentpage=self.currentpage - 1)
        def next_page(*args):
            self.populate_list_items(query=query, currentpage=self.currentpage + 1)
        previouspage.bind("<Button-1>", previous_page )
        nextpage.bind("<Button-1>", next_page )

root = Tk()
Notebook = Notebook(root)


config = Config()
config.validate()

root.geometry("%sx%s" %(root.winfo_screenwidth(), root.winfo_screenheight()))
my_gui = DataEntry(root)
root.mainloop()