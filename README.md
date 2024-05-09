# sqlalchemy-challenge
For this challenge, I used Python and SQLAlchemy to do a basic climate analysis and data exploration of a climate database. 
I specifically used SQLAlchemy ORM queries, Pandas, and Matplotlib. The analysis was split between precipitation analysis and station analysis. The precipitation analysis focused on querying 12 months of data and creating a barplot to visulize this data. The station data focused on querying the most active station in the data and performing analysis on that station. 

Following this analysis, I created a climate app using flask API. With this, I created the homepage and several routes, including precipitation, station, tobs (temperature observed), start and end. In each of the routes various queries were created and returned using jsonify().
