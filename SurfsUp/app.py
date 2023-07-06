# Import the dependencies.
# 1. import Flask
from flask import Flask, jsonify
#################################################
# Database Setup
#################################################
#%matplotlib inline
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import datetime as dt
import json

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine)
#probably dont need the line below but leave it here just in case for later.
#Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session_climate = Session(engine)

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return "Welcome to my 'Home' page!<br/> The available routes are:<br/>1.Precipitation<br/>2.Stations<br/>3.tobs<br/>4.Start<br/>5.End"

@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017,8,23)-dt.timedelta(days=365)
    results = session_climate.query(Measurement.date,Measurement.prcp).filter(Measurement.date>=prev_year).all()
    res_list = {date: prcp for date, prcp in results}
    session_climate.close()

    print("Server received request for 'Precipitation' page...")
    return jsonify(res_list)

@app.route("/api/v1.0/stations")
#use the same method as above turn stations call into a list

def stations():
    stats =(session_climate.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all())
    stats_list ={station: freq for station, freq in stats}
    #return only the keys as that is where station name lives
    keys = list(stats_list.keys())
    session_climate.close()
    print("Server received request for 'Stations' page...")
    return jsonify(keys)


@app.route("/api/v1.0/tobs")
#use the same method as above turn stations call into a list

def tobs():
    prev_year = dt.date(2017,8,23)-dt.timedelta(days=365)
    pre_hist =( session_climate.query(Measurement.date, Measurement.tobs).filter(Measurement.station=="USC00519281").filter(Measurement.date>=prev_year).all())
    session_climate.close()
#create for loop to craft dictionary with appropriate key and values date/tobs
    tobs_dict = []
    for date, temp in pre_hist:
        j_dict ={}
        j_dict["date"] = date
        j_dict["tobs"] = temp
        tobs_dict.append(j_dict)
    print("Server received request for 'tobs' page...")
    return jsonify(tobs_dict)

# 4. Define what to do when a user hits the /about route
@app.route("/api/v1.0/<start>")

def extremes(start):
    mean_temp = (session_climate.query(Measurement.station, func.avg(Measurement.tobs)).filter(Measurement.date>=start).all())
    
    min_temp = (session_climate.query(Measurement.station, func.min(Measurement.tobs)).filter(Measurement.date>=start).all())
    
    max_temp = (session_climate.query(Measurement.station, func.max(Measurement.tobs)).filter(Measurement.date>=start).all())
    
    session_climate.close()
    
    temp_dict = {}
    avg_t = {"TAVG": mean_temp[0][1]}
    low_t = {"TMIN": min_temp[0][1]}
    max_t = {"TMAX": mean_temp[0][1]}
    temp_dict.update(avg_t)
    temp_dict.update(low_t)
    temp_dict.update(max_t)
        
    return jsonify(temp_dict)

#this next block of code is very similar, except we add a filter for the end date as well
#helped with tutor and stack overflow and friends
@app.route("/api/v1.0/<start>/<end>")
def ending(start,end):
    mean_temp = (session_climate.query(Measurement.station, func.avg(Measurement.tobs)).filter(Measurement.date>=start).filter(Measurement.date<=end).all())
    
    min_temp = (session_climate.query(Measurement.station, func.min(Measurement.tobs)).filter(Measurement.date>=start).filter(Measurement.date<=end).all())
    
    max_temp = (session_climate.query(Measurement.station, func.max(Measurement.tobs)).filter(Measurement.date>=start).filter(Measurement.date<=end).all())
    
    session_climate.close()
    
    temp_dict = {}
    avg_t = {"TAVG": mean_temp[0][1]}
    low_t = {"TMIN": min_temp[0][1]}
    max_t = {"TMAX": mean_temp[0][1]}
    temp_dict.update(avg_t)
    temp_dict.update(low_t)
    temp_dict.update(max_t)
    
    return jsonify(temp_dict)



if __name__ == "__main__":
    app.run(debug=True)





#################################################
# Flask Setup
#################################################




#################################################
# Flask Routes
#################################################
