# SQLAlchemy_climate_data

Given a SQLite database of climate data in Honolulu, Hawaii, used Python and SQLAlchemy ORM queries for basic analysis and data exploration.

- - -

![precip](Resources/precipitation.JPG)

Last 12 months of precipitaion data across all stations.

- - -

![stats](Resources/sumstats.JPG)

Summary statistics for the precipitation data.

- - -

![station](Resources/station.JPG)

Frequency of temperature observations data from the most active station, and from the last 12 months.  Records for station 'USC00519281':

        Location: Waihee 837.5, HI US
        Lowest Temperature Recorded: 54.0
        Highest Temperature Recorded: 85.0
        Average Temperature Recorded: 71.66

- - -

**app.py:** Flask API based on SQLAlchemy queries developed during exploratory analysis.  Flask created routes resprectively return a JSON response object for precipitation, stations, temperature observations from the last year of data, or summary temperature statistics for a given start or start-end range of dates.