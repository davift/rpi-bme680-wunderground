# rpi-bme680-wunderground
Python code for RPi + BME680 to update the WeatherUnderground cloud.

This code is a customization of the example available on https://github.com/pimoroni/bme680-python to collect the data from the Pimoroni BME680 sensor in a Raspberry Pi and send to WUnderground.com

The idea behind this code is: sensor values may vary but sending them every second to the cloud does not make it the most accurate data. Instead, this code collects data for 60 seconds and only send the average every minute.

You can choose to run the code continuously, or make it end right after sending the data, and start it over every minute with cron.

I recommend the second option because in case your program stops you will need to intervene and run it again. Using cron to re-load it every minute not only synchronizes the data collection with the beginning of each minute but also allows you to make remote changes to the code that will be executed in the next minute. 

This code converts the unities to meet the WU cloud service requirements, and calculates the dew point based on temperature and humidity, which give a new variable to the weather station.

I am running this code in my RPi Zero W as a mini weather station outdoors in a sealed box but also protected from the rain by a roof.

Feel free to make comments and get in contact.
