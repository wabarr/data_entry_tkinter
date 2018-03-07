from peewee import *
from config import Config

config = Config()

db = SqliteDatabase(config.options["database path"])

class BaseRecord(Model):
    class Meta:
        database = db

class Record(BaseRecord):
    pass

# dynamically add fields to the Record class based on the parsed config file
for name, valuedict in config.options["fields"].items():
    if valuedict["datatype"]=="text":
        theField = CharField(null=valuedict["nullable"])
        # theField.add_to_class(Record, name)
    elif valuedict["datatype"]=="integer":
        theField = IntegerField(null=valuedict["nullable"])
        # theField.add_to_class(Record, name)
    elif valuedict["datatype"]=="decimal":
        theField = DecimalField(null=valuedict["nullable"])
        # theField.add_to_class(Record, name)
    elif valuedict["datatype"]=="datetime":
        theField = DateTimeField(null=valuedict["nullable"])
        # theField.add_to_class(Record, name)
