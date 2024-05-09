# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
station = Base.classes.station
measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/stations"
    )


@app.route("/api/v1.0/precipitation")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= query_date).all()

    session.close()

    # Convert query results to dictionary
    precipitation_dict = {date: prcp for date, prcp in results}

    return jsonify(precipitation_dict)

@app.route('/api/v1.0/stations')
def stations():
    # Create our session (link) from Python to the DB
    session = Session()

    # Query for the list of stations
    results = session.query(station.station).all()

    session.close()

    # Extract station names from query results
    stations_list = [result[0] for result in results]

    # Return JSON list of stations
    return jsonify(stations_list)

@app.route('/api/v1.0/tobs')
def tobs():
    # Create a sessionmaker
    session = Session()

    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query temperature observations for the most active station within the last 12 months
    temperature_data = session.query(measurement.date, measurement.tobs).\
        filter(measurement.station == 'USC00519281', measurement.date >= query_date).all()

    session.close()

    # Convert query results to a JSON list
    temperature_list = [{'date': date, 'tobs': tobs} for date, tobs in temperature_data]

    # Return JSON list of temperature observations
    return jsonify(temperature_list)



# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

