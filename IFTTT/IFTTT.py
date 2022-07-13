#! /usr/bin/python

# Imports
import time
import requests
import random

LINE_event_name = 'k07170132_Send_Line'
LINE_key = 'TnhIYY2oMyK15jMHP70Hx6OVTUjF-YhWViUtdm7KdG'

SHEETS_event_name = 'k07170132_Google_sheets'
SHEETS_key = 'TnhIYY2oMyK15jMHP70Hx6OVTUjF-YhWViUtdm7KdG'

session = requests.Session()

try:
    delay_time = int(input("Please enter the time splase of each data ( in second):"))

    PRE_SECOND=time.time()

    # Loop until users quits with CTRL-C
    while True:

        h0 = str(random.randint(0,30))
        t0 = str(random.randint(0,30))
 
        message = '你好'

        POST_SECOND=time.time()
        if (POST_SECOND - PRE_SECOND) >= delay_time :
            # Your IFTTT LINE_URL with event name, key and json parameters (values)
            LINE_URL='https://maker.ifttt.com/trigger/' + LINE_event_name + '/with/key/' + LINE_key
            r = session.post(LINE_URL, params={"value1":h0,"value2":t0,"value3":message})

            # # Your IFTTT SHEETS_URL with event name, key and json parameters (values)
            # SHEETS_URL='https://maker.ifttt.com/trigger/' + SHEETS_event_name + '/with/key/' + SHEETS_key
            # r = session.post(SHEETS_URL, params={"value1":h0,"value2":t0,"value3":message})

            PRE_SECOND=time.time()

            #Wait delay_time seconds before looping again
            print('Waiting for ' + str(delay_time) + ' seconds')


except KeyboardInterrupt:
    print(" Quit")
