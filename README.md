# Nextdose
New mag tag project. Lets me know if I took my insulin

I have had way too many times I have skipped my morning insulin. Now in the morning I have a new daily I cannot skip. 

The pills for the week holders are a great reminder. have not seen an equivilent for syringes.
I could 3d print a holder with spots to hold 2 syringes per day for mon-sun. But my tinkercad skills are non-existant, and pissed at my PRUSA.

Simple diplay: Next dose MONTH DAY {AM|PM}
- button 1: took dose - For the PM will advance to next day.  If pressed multiple times will do nothing.  For AM. will just change PM instead of AM.
- button 2: undo - reverts to previous state.

On power up if current state is not set will display AM message for the day. Otherwise will display current state.

In flash store current state and previous state.

Hit the undo and it display previous state.  If last state empty, do nothing.

# ToDo
- Fix TimeZome - done  
  Added both a tz offset andm tz name to secrets.py.  circuit python does not have pytz.
- Do not keep incrementing the day of the week on "Taken" press - done  
  use datatime.weekday() function
- Add check to make sure sleep_memory is correctly initiallized - done  
  Call nexttoken if sleep_memory is not initialized
 
# Lib
I copied another project, si I probably do not need this all.  Will need to fix it.

- adafruit_bitmap_font
- adafruit_datetime.mpy
- adafruit_display_text
- adafruit_fakerequests.mpy
- adafruit_io
- adafruit_magtag
- adafruit_minimqtt
- adafruit_ntp.mpy
- adafruit_portalbase
- adafruit_requests.mpy
- neopixel_spi.mpy
- simpleio.mpy
