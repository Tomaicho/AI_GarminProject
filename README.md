# AI_GarminProject

Folder dedicated to the first Smart Systems assignement (summer semester 2022-2023)

The goal was to monitorize one environment through the data collection from various sensors. I decided to use the sensors available from my own Garmin Forerunner 245 smartwatch. HR, sleep and stress, pedometer, spO2, etc. data was collected and processed. The access to the data was done through the Garmin Connect API, reutilizing and adapting the python code made available by cyberjunky at https://github.com/cyberjunky/python-garminconnect.

Basic analysis and notification triggers were then created to simulate a complex smart system that would evaluate the utilizer's performance and daily habits. Integration with Adafruit IO, IFTTT and OpenWeatherMap was also achieved.
