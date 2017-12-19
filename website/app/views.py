from app import app
from flask import Flask, render_template
import os
import well_model as wm    
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
    data['toto'] = "toto"
    return render_template('index.html', data=data)

@app.route('/well')
def well_data():
    entries = wm.get_entries(200)
    data =[[str(i.timestamp),i.watt1] for i in entries]
    data = {'row_data':data}
    last = wm.get_last()
    data['final_reading'] =last.timestamp
    return render_template('well.html', data=data)

