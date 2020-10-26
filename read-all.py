#!/usr/bin/env python

import bme680
import time
import os
import math

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except IOError:
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

# These calibration data can safely be commented
# out, if desired.

# print('Calibration data:')
for name in dir(sensor.calibration_data):

    if not name.startswith('_'):
        value = getattr(sensor.calibration_data, name)

#        if isinstance(value, int):
#            print('{}: {}'.format(name, value))

# These oversampling settings can be tweaked to
# change the balance between accuracy and noise in
# the data.

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

#print('\n\nInitial reading:')
for name in dir(sensor.data):
    value = getattr(sensor.data, name)

#    if not name.startswith('_'):
#        print('{}: {}'.format(name, value))

sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

# Up to 10 heater profiles can be configured, each
# with their own temperature and duration.
# sensor.set_gas_heater_profile(200, 150, nb_profile=1)
# sensor.select_gas_heater_profile(1)

#print('\n\nPolling:')
tem = 0
tem2 = 0
pre = 0
pre2 = 0
hum = 0
hum2 = 0
air = 0
air2 = 0
dew = 0
try:
    count = 0
    count2 = 1
    while True:
        if sensor.get_sensor_data():
            output = '{3:.0f}, {0:.2f} C, {1:.2f} hPa, {2:.2f} %'.format(sensor.data.temperature,sensor.data.pressure,sensor.data.humidity,count)

            if sensor.data.heat_stable:
		air = air + sensor.data.gas_resistance
                #print('{0}, {1} Ohms'.format(output,sensor.data.gas_resistance))

            #else:
                #print(output)

	tem = tem + sensor.data.temperature
	pre = pre + sensor.data.pressure
	hum = hum + sensor.data.humidity
	count = count + 1
	if count > 60:
		dew = (((math.log(hum/60/100))+((17.62*tem/60)/(243.12+tem/60)))*243.12)/(17.62-((math.log(hum/60/100))+((17.62*tem/60)/(243.12+tem/60))))
		# ITANAGRA
		os.system('curl "https://weatherstation.wunderground.com/weatherstation/updateweatherstation.php?ID=IITANA3&PASSWORD=HCHTQT46&dateutc=now&action=updateraw&humidity={2:.1f}&tempf={0:.1f}&baromin={1:.1f}&aqi={3:.0f}&dewptf={4:.1f}"'.format(tem/60*9/5+32,pre/60/33.86,hum/60,air/60/1000,dew*9/5+32))
                # TORONTO
		#os.system('curl "https://weatherstation.wunderground.com/weatherstation/updateweatherstation.php?ID=ITORON119&PASSWORD=BzmIDdxw&dateutc=now&action=updateraw&humidity={2:.1f}&tempf={0:.1f}&baromin={1:.1f}&aqi={3:.0f}&dewptf={4:.1f}"'.format(tem/60*9/5+32,pre/60/33.86,hum/60,air/60/1000,dew*9/5+32))
		count = 1
		count2 = count2 + 1
                tem2 = tem2 + tem/60
                pre2 = pre2 + pre/60
                hum2 = hum2 + hum/60
                air2 = air2 + air/60
                tem = 0
                pre = 0
                hum = 0
                air = 0
	if count2 > 10:
		os.system('curl "https://admin.dftorres.ca/weather.php?hum={2:.1f}&tem={0:.1f}&pre={1:.1f}&iaq={3:.0f}"'.format(tem2/10,pre2/10,hum2/10,air2/10000))
		count2 = 1
                tem = 0
                pre = 0
                hum = 0
                air = 0
		exit()

        time.sleep(1)

except KeyboardInterrupt:
    pass
