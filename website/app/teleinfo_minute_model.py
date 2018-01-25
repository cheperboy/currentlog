# -*- coding: utf8 -*-
from models import *
import teleinfo_model as Teleinfo
import datetime

def create(date_time, base, papp, iinst1, iinst2, iinst3):
    db_entry = TeleinfoMinute.create(base=base, papp=papp, iinst1=iinst1, iinst2=iinst2, iinst3=iinst3, timestamp=date_time)
    db_entry.save()

def get(nb):
    out = TeleinfoMinute.select().order_by(TeleinfoMinute.timestamp.desc()).limit(nb)
    return out[::-1]

def get_last():
    rec = get(1)
    if len(rec)>0:
        return rec[0]
    else:
        return None

def get_after_date(date):
    out = TeleinfoMinute.select().order_by(TeleinfoMinute.timestamp.desc()).where(TeleinfoMinute.timestamp > datetime.datetime(date.year, date.month, date.day, date.hour, date.minute))
    return out[::-1]

def get_between_date(begin, end):
    out = TeleinfoMinute.select().order_by(TeleinfoMinute.timestamp.desc()).where(TeleinfoMinute.timestamp > datetime.datetime(begin.year, begin.month, begin.day, begin.hour, begin.minute)).where(TeleinfoMinute.timestamp < datetime.datetime(end.year, end.month, end.day, end.hour, end.minute))
    return out[::-1]

def get_console(nb):
    entries = get(nb)
    out = ""
    for row in entries:
        out += "{} {} {} {} {}\n".format(row.timestamp,row.papp, row.iinst1, row.iinst2, row.iinst3)
    return out
#run every day

def process_archive_minute():
    print "process_archive_minute"
    # defini date de debut et de fin 
    # begin = (date du dernier record de la base Archive) + 1 minute
    # end = (maintenant) - 1 minute

    if get_last()== None:
        begin = Teleinfo.get_first().timestamp.replace(second=0, microsecond=0)
    else:
        begin = (get_last().timestamp + datetime.timedelta(minutes=1)).replace(second=0, microsecond=0)
    end = Teleinfo.get_last().timestamp - datetime.timedelta(minutes=1)
    print "\tbegin="+str(begin)
    print "\tend="+str(end)
    
    # while some old Logs to Archive
    while ((begin + datetime.timedelta(minutes=1)) < end):
        record_minute(begin)
        begin = begin + datetime.timedelta(minutes=1)

'''
recupere dans la base Logs l'ensenmble des objets dont la date est comprise entre 
begin et (begin + 1 minute)
Calcule des moyennes et enregistre
'''
def record_minute(begin):
    print "\t\trecord minute"
    #fake begin/end
#    begin = datetime.datetime.now() - datetime.timedelta(minutes=3)
    
    print "\t\tbegin="+str(begin)
    end = begin + datetime.timedelta(minutes=1)
    print "\t\tend="+str(end)
    base = 0
    papp = 0
    iinst1 = 0
    iinst2 = 0
    iinst3 = 0
    # get logs    
    logs = Teleinfo.get_between_date(begin, end)
    nb_logs = len(logs)
    print "\t\tnb_logs="+str(nb_logs)
    if nb_logs>0:
        for log in logs:
            if log.base > base: base = log.base # valeur la plus elevee de la serie
            papp += log.papp
            iinst1 += log.iinst1
            iinst2 += log.iinst2
            iinst3 += log.iinst3
        timestamp = begin
        # calcule des moyennes sur les serie
        papp = papp / nb_logs
        iinst1 = iinst1 / nb_logs
        iinst2 = iinst2 / nb_logs
        iinst3 = iinst3 / nb_logs
        # Save to db
        create(begin, base, papp, iinst1, iinst2, iinst3)


#print process_archive_minute()
