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

# create homepage
@app.route("/")
def welcome():
    # listing all the routes
    return (
        f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

# creating precipitation route
@app.route("/api/v1.0/precipitation")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # querying the last 12 months of data (same code from climate_starter)
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date > query_date).all()

    session.close()

    # create a dictionary from the results data
    precipitation = {date: prcp for date, prcp in results}

    return jsonify(precipitation)

# create stations route
@app.route('/api/v1.0/stations')
def stations():
    # Create our session (link) from Python to the DB
    session = Session()

    # Query for the list of stations
    results = session.query(station.station).all()

    session.close()

    # creating list of results
    stations = [result[0] for result in results]

    return jsonify(stations)

# create tobs route
@app.route('/api/v1.0/tobs')
def tobs():
    # Create our session (link) from Python to the DB
    session = Session()

    # setting our query date for last 12 months
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Querying the most active station for temperature over the last 12 months
    temperature_data = session.query(measurement.date, measurement.tobs).\
        filter(measurement.station == 'USC00519281', measurement.date >= query_date).all()

    session.close()

    # creating list from results
    temperature = [{'date': date, 'tobs': tobs} for date, tobs in temperature_data]

    return jsonify(temperature)

# create start and start/end routes 
#(got confirmation to do the two route setup this way through chatgpt)
@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')
def start_end(start, end = None):
    # Create our session (link) from Python to the DB
    session = Session()

    # if there is defined end date
    if end is not None:
        # querying the min, avg, and max of tempertaure between the defined start and end date
        results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
            filter(measurement.date >= start, measurement.date <= end).all()
    else: 
        # querying the min, avg, and max of tempertaure between the defined start and higher
        results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
            filter(measurement.date >= start).all()
     
    session.close()

    # Extract TMIN, TAVG, and TMAX from results
    tmin, tavg, tmax = results[0]

    # Create a dictionary with TMIN, TAVG, and TMAX
    temperature_data = {'TMIN': tmin, 'TAVG': tavg, 'TMAX': tmax}

    # Return JSON list of temperature data
    return jsonify(temperature_data)


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

