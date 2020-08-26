import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, distinct
import datetime as dt

from flask import Flask, jsonify

##Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

##Reflect an existing database into a new model
Base = automap_base()

##Reflect the tables
Base.prepare(engine, reflect=True)

##Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

##Flask Setup
app = Flask(__name__)

##Flask Routes
@app.route("/")
def welcome():
    """Here are all the available Routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        


    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    #Create session link from python to the database
    session = Session(engine)

    """Return dictionary of data with date as the key and prcp as the value."""
    results = session.query(Measurement.date,Measurement.prcp).all()

    session.close()

    #Create dictionary from data
    date_prcp = []
    for date, precipitation in results:
        container = {}
        container["date"] = date
        container["prcp"] = precipitation
        date_prcp.append(container)
    
    return jsonify(date_prcp)


@app.route("/api/v1.0/stations")
def stations():
    #Create session link from python to the database
    session = Session(engine)
    stations = session.query(distinct(Measurement.station)).all()
    session.close()

    stations_listed = list(np.ravel(stations))

    return jsonify(stations_listed)

@app.route("/api/v1.0/tobs")
def tobs():
    #Create session link from python to the database
    session = Session(engine)

    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    tobs_link = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281', Measurement.date > year_ago).all()
    
    session.close()
    
    tobs_listed = list(np.ravel(tobs_link))

    return jsonify(tobs_listed)

if __name__== '__main__':
    app.run(debug=True)