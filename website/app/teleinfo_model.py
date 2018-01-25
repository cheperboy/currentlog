from models import *
import datetime

def create(date_time, base, papp, iinst1, iinst2, iinst3):
    db_entry = Teleinfo.create(base=base, papp=papp, iinst1=iinst1, iinst2=iinst2, iinst3=iinst3, timestamp=date_time)
    db_entry.save()

def get(nb):
    out = Teleinfo.select().order_by(Teleinfo.timestamp.desc()).limit(nb)
    return out[::-1]

def get_last():
    rec = get(1)
    if len(rec)>0:
        return rec[0]
    else:
        return None

def get_first():
    out = Teleinfo.select().order_by(Teleinfo.timestamp.asc()).limit(1)
    return out[::-1][0]

def get_after_date(date):
    out = Teleinfo.select().order_by(Teleinfo.timestamp.desc()).where(Teleinfo.timestamp > datetime.datetime(date.year, date.month, date.day, date.hour, date.minute))
    return out[::-1]

def get_between_date(begin, end):
    out = Teleinfo.select().order_by(Teleinfo.timestamp.desc()).where(Teleinfo.timestamp > datetime.datetime(begin.year, begin.month, begin.day, begin.hour, begin.minute)).where(Teleinfo.timestamp < datetime.datetime(end.year, end.month, end.day, end.hour, end.minute))
    return out[::-1]

def get_console(nb):
    entries = get(nb)
    out = ""
    for row in entries:
        out += "{} {} {} {} {}\n".format(row.timestamp,row.papp, row.iinst1, row.iinst2, row.iinst3)
    return out

#log_data(datetime.datetime.now(), 0, 0, 0, 0, 0)
#print get_console(10)
#print get_entries(1)
#print get_csv(1000)