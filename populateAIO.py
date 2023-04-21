import pandas as pd
from Adafruit_IO import Client, Feed
import json

def sendToAIO(feed, value):
    # Define your Adafruit IO credentials
    ADAFRUIT_IO_USERNAME = "Tomacho"
    ADAFRUIT_IO_KEY = "aio_GJgL76zsvDdBOopQWZpRHCJPFGqd"

    # Create an instance of the Adafruit IO client
    aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
    aio.send_data(feed, value)
