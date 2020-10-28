import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# import Flask
from flask import Flask, jsonify

# database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask setup: create app
app = Flask(__name__)

# define the index route/home page
@app.route("/")
def home():
    print("Received request for 'Home' page...")
    return (
        f"Welcome to the Home Page!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # create our session (link) from Python to the DB
    session = Session(engine)

    ### return a dictionary using date as the key and prcp as the value ###
    # query date and prcp
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    # create a dictionary of the tuples list
    all_precipitation = dict(results)
    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def stations():
    # create our session (link) from Python to the DB
    session = Session(engine)
    
    # query all the stations
    results = session.query(Station.name).all()
    session.close()
    
    # convert list of tuples into a normal list
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def temperature():
    # create our session (link) from Python to the DB
    session = Session(engine)
    
    # query the most active station for the last year of data
    sel = [Measurement.station,
        func.count(Measurement.tobs)]

    results = session.query(*sel).\
        filter(func.strftime("%Y", Measurement.date) == "2017").\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.tobs).desc()).first()

    # query dates and temperature observations for the previous year
    sel2 = [Measurement.station,
        Measurement.date,
        Measurement.tobs]

    results2 = session.query(*sel2).\
        filter(func.strftime("%Y", Measurement.date) == "2016").\
        filter(Measurement.station == results[0]).\
        order_by(Measurement.date).all()
    session.close()

    # create a dictionary from the row data and append to
    # a list of all_temp
    all_temp = []
    for station, date, tobs in results2:
        temp_dict = {}
        temp_dict["station"] = station
        temp_dict["date"] = date
        temp_dict["tobs"] = tobs
        all_temp.append(temp_dict)
    return jsonify(all_temp)

@app.route("/api/v1.0/<start>")
def start(start):
    # create our session (link) from Python to the DB
    session = Session(engine)
    
    # query the min temp, avg temp, and max temp for
    # all dates greater than and equal to start date
    sel = [Measurement.date,
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)]

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        group_by(Measurement.date).all()
    session.close()

    # create a dictionary from the row data and append to
    # a list of all_dates
    all_dates = []
    for x in range(len(results)):
        dates_dict = {}
        dates_dict["date"] = results[x][0]
        dates_dict["min"] = results[x][1]
        dates_dict["avg"] = round(results[x][2], 2)
        dates_dict["max"] = results[x][3]
        all_dates.append(dates_dict)
    return jsonify(all_dates)
    
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # create our session (link) from Python to the DB
    session = Session(engine)
    
    # query the min temp, avg temp, and max temp for
    # all dates between the given start and end dates
    sel = [Measurement.date,
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)]

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).\
        group_by(Measurement.date).all()
    session.close()

    # create a dictionary from the row data and append to
    # a list of range_dates
    range_dates = []
    for x in range(len(results)):
        dates_dict = {}
        dates_dict["date"] = results[x][0]
        dates_dict["min"] = results[x][1]
        dates_dict["avg"] = round(results[x][2], 2)
        dates_dict["max"] = results[x][3]
        range_dates.append(dates_dict)
    return jsonify(range_dates)
    
if __name__ == "__main__":
    app.run(debug=True)
