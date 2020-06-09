# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 14:50:07 2020

@author: aditm
"""

from flask import Flask, jsonify
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import pandas as pd

#%% Database Setup
engine = create_engine("sqlite:///hawaii.sqlite")
#Reflect an existing database into a new model
Base = automap_base()
#Reflect the tables
Base.prepare(engine, reflect=True)
#Check for the Table Names
print('Testing -- Looking for the keys(table)')
print(Base.classes.keys())
print('end test')
#conn = engine.connect()
#%% Save a reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station
#%%Flask Set Up
app = Flask(__name__)
#%%
@app.route("/")
def welcome():
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

#%%    
@app.route("/api/v1.0/precipitation")
def precipitation():
    result = pd.read_sql('SELECT date, prcp FROM measurement WHERE date BETWEEN "2016-08-23" AND "2017-08-23"', engine)
    result_json = result.to_json(orient='records')
    return result_json
#%%
@app.route("/api/v1.0/stations")
def station():
    station_result = pd.read_sql("SELECT station FROM station", engine)
    station_result_json = station_result.to_json(orient='records')
    return station_result_json
#%%
@app.route("/api/v1.0/tobs")
def tobs():
    Measurement_Station = pd.read_sql("SELECT date, tobs FROM measurement INNER JOIN station on measurement.station = station.station WHERE measurement.station == 'USC00519281' AND date BETWEEN '2016-08-23' AND '2017-08-23'", engine)
    tobs_result_json = Measurement_Station.to_json(orient='records')
    return tobs_result_json
#%%
@app.route("/api/v1.0/<start>")
def start(start):
    conn = engine.connect()
    start_result = pd.read_sql("SELECT MIN(tobs) as 'Mininum', MAX(tobs) as 'Maximum', AVG(tobs) as 'Average' FROM measurement WHERE measurement.date >= (measurement.date = 'start')", conn)
    start_result_json = start_result.to_json(orient='records')
    return start_result_json
    
        
#%%
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    start_result = pd.read_sql("SELECT MIN(tobs) as 'Mininum', MAX(tobs) as 'Maximum', AVG(tobs) as 'Average' FROM measurement WHERE date >= (measurement.date == 'start') AND date < (measurement.date == 'end')", engine)
    start_result_json = start_result.to_json(orient='records')
    return start_result_json

#%%    
if __name__ == "__main__":
    app.run(debug=True)
        