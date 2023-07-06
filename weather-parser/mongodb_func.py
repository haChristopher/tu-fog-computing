import pandas as pd
from pymongo import MongoClient
import pymongo
import certifi


db_ = "QNqVEUJUtqhegG6k"
db_user = "fog"
# Connect to MongoDB
url = f"mongodb+srv://{db_user}:{db_}@fog.m9hlcut.mongodb.net/?retryWrites=true&w=majority"
cluster = pymongo.MongoClient(url, tlsCAFile=certifi.where(), connect=False)
db = cluster['weather-storage'] 

collection = db['weather_v3']

# Read CSV file
data = pd.read_csv('weather.csv')

# Convert DataFrame to dictionary and insert into MongoDB
data_dict = data.to_dict(orient='records')
collection.insert_many(data_dict)

# Close the MongoDB connection
cluster.close()
