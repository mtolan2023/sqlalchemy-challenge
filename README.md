# sqlalchemy-challenge
Flask API/Python delivering data from Hawaiian weather stations

This repo contains the "SurfsUp" project folder, where Jupyter Notebook, python app and Resources folder for the Module 10 challenge are found.

1. climate_analysis - Jupyter Notebook - includes anaylsis of the hawaii sqlite db:
  - Average Precepitation for the most recent year of data (8/23/2016-8/23/2017) by date.
  - Station count
  - Identification of most active station ('USC00519281', WAIHEE)
  - Max, Min and Average Temp for most active station
  - Histogram of Temeratures over the most recent year for the most active station

2. app.py - Python/Flask - filters and formats data for JSON queries. Available routes:
  - /api/v1.0/precipitation - provides precipation data from most recent year as dictionary.
  - /api/v1.0/stations - provides a list of the weather stations in the database.
  - /api/v1.0/tobs - provides the temperature data for the most recent year for the most active station (('USC00519281', WAIHEE).
  - /api/v1.0/<start>(user_input_start_date) - returns Min, Max and Average Temperatures for the most active station for any date given by user.
  - /api/v1.0/<start>(user_input_start_date)/<end>(user_input_end_date) - returns Min, Max and Average Temps for any date range given by user.
  
 3. Resources folder contains csvs and db used in analysis:
  - hawaii_measurements.csv - contains temp/precip data for all stations
  - hawaii_stations.csv - contains station names, ids, locations
  - hawaii.sqlite - db used for data queries.




Citations:
  Code used to find one year before date in Jupyter Notebook and app.py
- https://stackoverflow.com/questions/55183235/get-the-one-year-before-date-for-a-given-date-in-python
