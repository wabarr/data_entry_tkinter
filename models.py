from peewee import *

db = SqliteDatabase("DIK-database.sqlite3")


class BaseRecord(Model):
    class Meta:
        database = db

class Record(BaseRecord):
    name = CharField()