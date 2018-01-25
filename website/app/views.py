from app import app
from flask import Flask, render_template, json, jsonify, g
import os
import well_model as wm
import teleinfo_model as Teleinfo
import models
import teleinfo_minute_model as TeleinfoMinute
import datetime
import time


@app.route('/')
@app.route('/watts')
def watts_data():
    entries = wm.get_entries(3000)
    data = []
    for i in entries:
        data.append([i.timestamp,i.watt1,i.watt2])
    
    data = {'row_data':data}
    last = wm.get_last()
    data['final_reading'] =last.timestamp
    return render_template('teleinfo/index3.html', data=data)

@app.route('/teleinfo')
def teleinfo():
    data_1 = []
    datetime_1 = datetime.datetime.now() - datetime.timedelta(minutes=15)
    entries_1 = Teleinfo.get_after_date(datetime_1)
    for i in entries_1:
        second = str(i.timestamp).split(':')[2].split('.')[0]
        data_1.append([i.timestamp, second, i.papp, i.iinst1, i.iinst2, i.iinst3])
    data_1 = {'row_data':data_1}

    data_2 = []
    datetime_2 = datetime.datetime.now() - datetime.timedelta(minutes=120)
    entries_2 = TeleinfoMinute.get_after_date(datetime_2)
    for i in entries_2:
        second = str(i.timestamp).split(':')[2].split('.')[0]
        data_2.append([i.timestamp, second, i.papp, i.iinst1, i.iinst2, i.iinst3])
    data_2 = {'row_data':data_2}

    options = []
    options = {'row_data':options}
    options['hour_format'] = "HH:mm"
    return render_template('teleinfo/index.html', data_15=data_1, data_1h=data_2, options=options)

@app.route('/test')
def testchart():
    entries = Teleinfo.get_entries(1000)
    data = []
    for i in entries:
        second = str(i.timestamp).split(':')[2].split('.')[0]
        data.append([i.timestamp, second, i.papp, i.iinst1, i.iinst2, i.iinst3])
    
    data = {'row_data':data}
    last = Teleinfo.get_last()
    data['final_reading'] = str(last.timestamp)
    return render_template('test/index.html', data=data)

@app.route('/json')
def json():
    entries = TeleinfoMinute.get_entries(10000)
    data = []
    for i in entries:
        second = str(i.timestamp).split(':')[2].split('.')[0]
        data.append([i.timestamp, second, i.papp, i.iinst1, i.iinst2, i.iinst3])
    return jsonify({'rdata': data})

@app.route('/well')
def well_data():
    entries = wm.get_entries(200)
    data =[[str(i.timestamp),i.watt1] for i in entries]
    data = {'row_data':data}
    last = wm.get_last()
    data['final_reading'] =last.timestamp
    return render_template('well.html', data=data)

# Request handlers -- these two hooks are provided by flask and we will use them
# to create and tear down a database connection on each request.
@app.before_request
def before_request():
    g.db = models.db
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response

