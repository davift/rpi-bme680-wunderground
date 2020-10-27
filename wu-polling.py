#!/usr/bin/env python

import bme680
import time
import os
import math

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except IOError:
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

for name in dir(sensor.calibration_data):
    if not name.startswith('_'):
        value = getattr(sensor.calibration_data, name)

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)

# ADD HERE THE CREDENTIALS TO THE DEVICE ALREADY ADDED TO THE WEATHER UNDERGROUND DASHBOARD (https://www.wunderground.com/member/devices):
wu_id = 'ID'
wu_key = 'Key'

tem = 0
pre = 0
hum = 0
dew = 0
try:
    count = 1
    while True:
	tem = tem + sensor.data.temperature
	pre = pre + sensor.data.pressure
	hum = hum + sensor.data.humidity
	count = count + 1
	if count > 60:
		dew = (((math.log(hum/60/100))+((17.62*tem/60)/(243.12+tem/60)))*243.12)/(17.62-((math.log(hum/60/100))+((17.62*tem/60)/(243.12+tem/60))))
		os.system('curl "https://weatherstation.wunderground.com/weatherstation/updateweatherstation.php?ID={4}&PASSWORD={5}&dateutc=now&action=updateraw&tempf={0:.1f}&baromin={1:.5f}&humidity={2:.1f}&dewptf={3:.1f}"'.format(tem/60*9/5+32,pre/60*0.02952998,hum/60,air/60/1000,dew*9/5+32,wu_id,wu_key))
		count = 1
                tem = 0
                pre = 0
                hum = 0
		# COMMENT THIS LINE TO KEEP IT IN LOOPING OR USER CRON TO RELOAD IT EVERY MINUTE
		exit()
		# TO CREATE THE CRON RE-LOAD ROUTINE ISSUE THE COMMAND: crontab -e
		# AND ADD THIS LINE AT THE END: * * * * * /home/pi/read-all.py > /dev/null 2>&1

        time.sleep(1)

except KeyboardInterrupt:
    pass
