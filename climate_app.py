#Import libraries

from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import datetime as dt
import pandas as pd
import numpy as np

#create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#reflect database into new model
Base = automap_base()

#reflect tables
Base.prepare(engine,reflect = True)

#Reference each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#create a session
session = Session(engine)


#setup flask
app = Flask(__name__)

#create route
@app.route("/")

def climate_app():
    return(
    f"Available Routes:<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/<start><br/>"
    f"/api/v1.0/<end>"
    )

@app.route(f"/api/v1.0/precipitation")
def prcp():
    #query percipitations
    data = session.query(Measurement).all()
    
    #create a dictionary from query
    percipitation = []
    for rainfall in data:
        prcp_dict = {}
        prcp_dict['date'] = rainfall.date
        prcp_dict["prcp"] = rainfall.prcp
        percipitation.append(prcp_dict)
    return jsonify(percipitation)
    
@app.route(f"/api/v1.0/stations")
def stations():
    #query stations
    station_query = session.query(Station.station).all()
    
    #create list
    station_list = list(np.ravel(station_query))

    return jsonify(station_list)

@app.route(f"/api/v1.0/tobs")
def temp():
    date_temp = []
    temp_range = session.query(Measurement.tobs).filter(Measurement.date >= "08-23-2017").all()
    year_tobs = list(np.ravel(temp_range))
    return jsonify(year_tobs)


@app.route("/api/v1.0/<start>")
def start_temp(start):
    # create query to obtain min,avg and max
    temp_data = (session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),
     func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    )
    
    return jsonify(temp_data)

    

@app.route("/api/v1.0/<start>/<end>")
def range_temp(start, end):
 # #create query to obtain temps from a date range
    temp_math = (session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),
     func.max(Measurement.tobs)).filter((Measurement.date >= start, Measurement.date <= end)).all()
     )
    
    return jsonify(temp_math)

if __name__ == "__main__":
    app.run(debug=True)
