# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt
from datetime import timedelta

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>(user_input_start_date)<br/>"
        f"/api/v1.0/<start>(user_input_start_date)/<end>(user_input_end_date)<br/>" 
        f" * Note - Dates must be entered in YYYY-mm-dd format" 
        f"Data available from 2010-01-01 through 2017-08-23"
    )

@app.route("/api/v1.0/precipitation")
def precip():
    # Create our session (link) from Python
    session = Session(engine)
    # Find the most recent date in the data set.
    last = session.query(Measurement.date).group_by(Measurement.date).order_by(desc(Measurement.date)).first()
    # Design a query to retrieve the last 12 months of precipitation data and plot the results. 
    # Starting from the most recent data point in the database. 
    end_date = last.date
    # Calculate the date one year from the last date in data set.
    start_date = (dt.datetime.strptime(end_date, '%Y-%m-%d') - dt.timedelta(days=365)).strftime('%Y-%m-%d')
    # Perform a query to retrieve the data and precipitation scores
    dates =  session.query(Measurement).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date)\
             .with_entities(Measurement.date, Measurement.prcp)
    session.close()
    #create dictionary from query using date as key and precip as value
    dict = {date.date: date.prcp for date in dates}
    return jsonify(dict)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    #query all station names from Station class
    station = session.query(Station.name).all()
    session.close()
    #convert tuples to list
    station_names = list(np.ravel(station))
    return jsonify(station_names)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    # Determine most recent date in dataset
    last = session.query(Measurement.date).group_by(Measurement.date).order_by(desc(Measurement.date)).first() 
    end_date = last.date
    # Calculate the date one year from the last date in data set.
    start_date = (dt.datetime.strptime(end_date, '%Y-%m-%d') - dt.timedelta(days=365)).strftime('%Y-%m-%d')
    # Perform a query to retrieve the data from the most active station
    active_station =  session.query(Measurement).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date)\
             .filter(Measurement.station == 'USC00519281').all()
    session.close()
    
    #add temp data from active station to list
    temp_list = []
    for row in active_station:
        temp_list.append(row.tobs)

    return jsonify(temp_list)

@app.route("/api/v1.0/<start>")
def temp(start):
    #error code for dates outside of date range and/or misformatted dates
    if start < "2010-01-01" or start > "2017-08-23":
        return jsonify({"error": f"Date {start} out of range (2010-01-01 through 2017-08-23). Check date and format (YYYY-mm-dd)"}), 404
    #if no error present, run this:
    else:
        session = Session(engine)
        #query measurement.tobs for all dates beginning with start date.
        start_data = session.query(Measurement.tobs).filter(Measurement.date >= start)
        session.close() 

        #add all temp readings to list
        start_list = []
        for row in start_data:
            start_list.append(row.tobs)
        #find min/max/avg of items in list
        tmin = min(start_list)
        tmax = max(start_list)
        tavg = sum(start_list) / len(start_list)
        #return as list
        start_output = [tmin, tmax, tavg]

        return jsonify(start_output)

    


@app.route("/api/v1.0/<start>/<end>")
def range(start, end):
    # error code if start date is out of range or misformatted
    if start < "2010-01-01" or start > "2017-08-23":
        return jsonify({"error": f"Date {start} out of range (2010-01-01 through 2017-08-23) Check date and format (YYYY-mm-dd)"}), 404
    # error code if end date is out of range or misformatted
    elif end < "2010-01-01" or end > "2017-08-23":
        return jsonify({"error": f"Date {end} out of range (2010-01-01 through 2017-08-23) Check date and format (YYYY-mm-dd)"}), 404
    # error code if dates are out of order (end date first)
    elif start > end:
        return jsonify({"error": f"Start Date ({start}) and End Date ({end}) out of order"}), 404

    # if no errors present, move forward with query
    else:
        
        session = Session(engine)
        # query all temp info between start and end dates (inclusive)
        range_data = session.query(Measurement.tobs).filter(Measurement.date >= start)\
             .filter(Measurement.date <= end )
        session.close()
        # add temp data to list
        range_list = []
        for row in range_data:
            range_list.append(row.tobs)
        # find min/max/avg of items in list
        tmin = min(range_list)
        tmax = max(range_list)
        tavg = sum(range_list) / len(range_list)
        # return as list
        start_end_output = [tmin, tmax, tavg]

        return jsonify(start_end_output)
    



if __name__ == '__main__':
    app.run(debug=True)