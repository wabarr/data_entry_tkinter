from Tkinter import Tk, Label, Button, Frame, Entry
from models import Record, db
import yaml

with open("config.yml", "r") as configfile:
    config = yaml.load(configfile)
    configfile.close()

class DataEntry:

    def __init__(self, master):
        self.master = master
        self.master.title(config["project title"])

        if not Record.table_exists():
            db.create_tables([Record])

        self.buttons = Frame(master)
        self.buttons.grid(row=0, column=0)
        Button(self.buttons, text="Add Record", command=self.add_record).grid(row=1, column=0)
        Button(self.buttons, text="Close", command=master.quit).grid(row=1, column=1)

        self.items = Frame(master)
        items_label = Label(self.items, text="Items in database", font=("Arial", 20, 'bold'))
        items_label.grid(columnspan=2)
        self.items.grid(row=2,column=0)
        self.populate_items()

    def populate_items(self):
        for record in enumerate(Record.select()):
            Label(self.items, text=record[1].id).grid(row=record[0] + 2, column=0)
            Label(self.items, text=record[1].name).grid(row=record[0] + 2, column=1)
            #Button(self.items,text="Delete Record").grid(row=record[0] + 2, column=3, command=self.delete_record(record[1].id))

    def add_record(self):
        Record.create(name="new_record")
        self.populate_items()

    def delete_record(self, theID):
        Record.select().where(Record.id == theID).get().delete_instance()
        self.populate_items()

root = Tk()
my_gui = DataEntry(root)
root.mainloop()