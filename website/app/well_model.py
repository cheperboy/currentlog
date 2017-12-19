from peewee import *  # see http://docs.peewee-orm.com/en/latest/
import os

BASE = "/home/pi/currentlog/db"
DATABASE = "watts3.db"

db = SqliteDatabase(os.path.join(BASE,DATABASE), threadlocals=True) #returns a peewee.Database instance

class logs(Model):
    """class defining the model"""
    timestamp = DateTimeField()
    watt1 = FloatField()
    watt2 = FloatField()
    class Meta:
        database=db
 
def log_data(date_time, watt1, watt2):
    initialize_db()
    db_entry = logs.create(watt1=watt1,watt2=watt2,timestamp=date_time)
    db_entry.save()
 
def initialize_db():
    """safely initialize database if it is not there"""
    db.connect()
    db.create_tables([logs], safe=True)  #safe checks whether database exists
    db.close()
def get_entries_desc(num_entries):
    """get a num_entries length list of entries, starting with the most recent"""
    a=logs.select().order_by(logs.timestamp.desc()).limit(num_entries)

def get_entries(num_entries):
    """get a num_entries length list of entries, starting with the most recent,
    but sorted oldest to newest"""
    out = logs.select().order_by(logs.timestamp.desc()).limit(num_entries)
    return out[::-1]

def get_last():
    """get the last entry"""
    return get_entries(1)[0]

def get_csv(num_entries):
    entries = get_entries(num_entries)
    out = ""
    for row in entries:
        out += "{},{}\n".format(row.timestamp,row.watt1)
    return out

#log_data(datetime.datetime.now(), 1111, 2222)
#initialize_db
#print get_entries(1)