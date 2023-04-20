import pandas as pd
from Adafruit_IO import Client, Feed
import json

def sendToAIO(feed, value):
    # Define your Adafruit IO credentials
    ADAFRUIT_IO_USERNAME = "Tomacho"
    ADAFRUIT_IO_KEY = "aio_rAGc53fd3SmDbGK5ZIr4LH97LQDq"

    # Create an instance of the Adafruit IO client
    aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
    aio.send_data(feed, value)

# Read in the data from the CSV file
# data = pd.read_csv('combined_today.csv')
# print(data)

# Iterate through the rows of the data and send each column value to the appropriate feed
# for row in data.iterrows():
#     # Get the values from the timestamp and heart-rate columns
#     print(row[1].loc['timestamp'])
#     print(row[1].loc['heart_rate'])
#     timestamp = row[1].loc['timestamp']
    
#     if row[1].loc['heart_rate'] != 'nan':
#         hr_value = row[1].loc['heart_rate']
#         print(hr_value)
#         # Send the values to the appropriate feeds
#         aio.send_data('garmin-data.timestamp', timestamp)
#         aio.send('garmin-data.heart-rate', str(hr_value))
