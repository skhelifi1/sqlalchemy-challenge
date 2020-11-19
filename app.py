import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base=automap_base()
Base.prepare(engine, reflect=True)
Measurement= Base.classes.measurement
Station=Base.classes.station
app = Flask(__name__)

@app.route("/")
def Home_page():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation>"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        )


@app.route("/api/v1.0/precipitation>")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of dates and its corresponding precipitation"""
    
    precip_list= session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>=one_year_ago)

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    date_precip= []
    for date, prcp in precip_list:
        date_precip_dict = {}
        date_dict["date"] = date
        precip_dict["prcp"] = prcp
        date_precip.append(date_precip_dict)

    return jsonify(date_precip)
    
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations from the dataset"""
    stations_list = session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    session.close()
    # convert a tuple list into a normal list
    stations_lst= list(np.ravel(stations_list))
    return jsonify(stations_lst)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    """Return the dates and temperature observations of the most active station for the last year of data"""

    temp_list=session.query(Measurement.tobs).filter(Measurement.station=='USC00519281').filter(Measurement.date>=one_year_ago).all()
    session.close()

    temp_lst= list(np.ravel(temp_list))
    return jsonify(temp_lst)

if __name__ == '__main__':
    app.run(debug=True)
