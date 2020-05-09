import serial
from datetime import datetime
import sys
from Adafruit_IO import Client, RequestError, Feed
import settings

ADAFRUIT_IO_KEY = settings.ADAFRUIT_IO_KEY
ADAFRUIT_IO_USERNAME = settings.ADAFRUIT_IO_USERNAME
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

feed_name = 'solar-battery-feed'

try:
    battery_feed = aio.feeds(feed_name)
except RequestError: # Doesn't exist, create a new feed
    battery_feed = Feed(name=feed_name)
    battery_feed = aio.create_feed(battery_feed)

ser = serial.Serial('/dev/ttyACM0')  # open serial port
print(ser.name)         # check which port was really used

with open("%s.csv" % datetime.now().strftime("%d%m%Y_%H:%M:%S"), "w") as fh:
    fh.write('time,vbatt\n')
    while(True):
        line = ser.readline().decode("utf-8").rstrip()
        if line.isdigit():

            batVal = int(line) / 1000
            aio.send_data(battery_feed.key, batVal)

            fh.write(datetime.now().strftime("%d%m%Y_%H:%M:%S") + ',' + str(line) + '\n')
            print(datetime.now().strftime("%d%m%Y_%H:%M:%S") + ',' + str(line))
            fh.flush()
            sys.stdout.flush()


ser.close()

