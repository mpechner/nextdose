import board
#import neopixel
import time
import busio
import math
import json
from adafruit_magtag.magtag import MagTag
from secrets import secrets
from time import sleep
from adafruit_datetime import datetime, timedelta
from gc import collect
import alarm
from adafruit_portalbase import PortalBase
import adafruit_ntp
import socketpool
import wifi
#from alarm import PinAlarm

dow = ["Monday", "Tuesday","Wednesday", "Thursday", "Friday", "Saturday", "Sunday" ]

#resp = json.loads('{"type":"Point","coordinates":[-178.3804,-20.6238,559.13]}')
#print(resp)

'''
sleep_memory bytes
cur
0 = 1:am 0:pm
1 = date
2 day

prev
3 = 1:am 0:pm
4 = date
5 day



'''


#############################

def get_cur_time():
    wifi.radio.connect(secrets["ssid"], secrets["password"])

    pool = socketpool.SocketPool(wifi.radio)
    ntp = adafruit_ntp.NTP(pool, tz_offset=0)
    return ntp

def deep_sleep():
    last_line = " Taken                     Undo"
    magtag.add_text(  # text_font="/fonts/Lato-Bold-ltd-25.bdf",
        text_position=(1, 121),
        is_data=False,
        text=last_line
    )

    alarms.append(alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 43200))
    alarm.exit_and_deep_sleep_until_alarms(*alarms)

def clear_display():
    magtag.graphics.set_background(0xFFFFFF)

def flashit(fillset):
    for ii in range(0, 4):
        magtag.peripherals.play_tone(440, 0.15)
        magtag.peripherals.neopixels.fill(fillset)
        time.sleep(.25)
        magtag.peripherals.neopixels.fill((0, 0, 0))
        time.sleep(.25)

def print_message(doCurrent):
    global dow

    offset = 0
    if not doCurrent:
        offset = 3
    print("offset = ", offset)


    print("%d off %d %d %d" % (offset, alarm.sleep_memory[0 + offset], alarm.sleep_memory[1 + offset], alarm.sleep_memory[2+offset]))
    print("cur %d %d %d" % (alarm.sleep_memory[0], alarm.sleep_memory[1], alarm.sleep_memory[2]))
    print("prewv %d %d %d" % (alarm.sleep_memory[3], alarm.sleep_memory[4], alarm.sleep_memory[5]))

    dostime = 'PM'
    if alarm.sleep_memory[0 + offset] == 1 :
        dostime = 'AM'

    data_str = "%s  %d  %s" %(dow[alarm.sleep_memory[2 + offset]], alarm.sleep_memory[1 + offset], dostime)
    print("msg:", data_str)

    magtag.add_text(
        text_position=(15, 45),
        is_data=False,
        text_scale = 2
    )
    magtag.set_text(data_str, index = 1, auto_refresh=False)

def next_dose():

    curtime = get_cur_time()
    newtime = curtime.datetime

    # initialize  sleep_memory
    if alarm.sleep_memory[1] < 1 or alarm.sleep_memory[1] > 31:
        print("set initial time")
        alarm.sleep_memory[0] = 1
        if newtime.tm_hour > 2:
            alarm.sleep_memory[0] = 0
        alarm.sleep_memory[1] = newtime.tm_mday
        alarm.sleep_memory[2] = newtime.tm_wday
        alarm.sleep_memory[3] = 0
        alarm.sleep_memory[4] = 0
        alarm.sleep_memory[5] = 0
        print_message(True)
        return

    # only change from AM to PM
    if alarm.sleep_memory[0] == 1 :
        alarm.sleep_memory[3] = 1
        alarm.sleep_memory[0] = 2
        print_message(True)
        return

    #Flip to next day
    dt_day = datetime(newtime.tm_year, newtime.tm_mon, newtime.tm_mday, newtime.tm_hour, newtime.tm_min, newtime.tm_sec)
    nextday = dt_day + timedelta(days = 1)
    print("next day ", type(nextday), nextday)

    alarm.sleep_memory[3] = alarm.sleep_memory[0]
    alarm.sleep_memory[4] = alarm.sleep_memory[1]
    alarm.sleep_memory[5] = alarm.sleep_memory[2]

    alarm.sleep_memory[0] = 1
    alarm.sleep_memory[1] = nextday.day
    alarm.sleep_memory[2] = alarm.sleep_memory[2] + 1
    if alarm.sleep_memory[2] > 6:
        alarm.sleep_memory[2] = 0

    print_message(True)


def undo_dose():
    global dow
    if alarm.sleep_memory[4] < 1 or alarm.sleep_memory[4] > 31:
        print("UNDO RETURN ", alarm.sleep_memory[4])
        print_message(True)
        return
    alarm.sleep_memory[0] = alarm.sleep_memory[3]
    alarm.sleep_memory[1] = alarm.sleep_memory[4]
    alarm.sleep_memory[2] = alarm.sleep_memory[5]
    print_message(True)


buttons = [board.BUTTON_A, board.BUTTON_C]
alarms = [alarm.pin.PinAlarm(pin=pin, value=False, pull=True) for pin in buttons]

magtag = MagTag()

if magtag.peripherals.battery < 2.9:
    for ii in range(0, 10) :
        magtag.peripherals.play_tone(3000, 1.0)
        sleep(1)
    magtag.add_text(
        text_position=(40, 60),
        is_data=False,
        text_scale=3,
        text="BATTERY LOW"
    )
    magtag.exit_and_deep_sleep(7200)

magtag.add_text(
    text_position=(5,11),
    is_data=False,
    text_scale = 2)
magtag.set_text("When is next dose?", index=0, auto_refresh=False)

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

#print(type(alarm.wake_alarm), alarm.wake_alarm)
if isinstance(alarm.wake_alarm, alarm.pin.PinAlarm): #PinAlarm
    if alarm.wake_alarm.pin == board.BUTTON_A:
      next_dose()
    elif alarm.wake_alarm.pin == board.BUTTON_C:
      undo_dose()
else:
    print_message(True)
deep_sleep()
