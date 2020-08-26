import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"


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

if __name__== '__main__':
    app.run(debug=True)

    