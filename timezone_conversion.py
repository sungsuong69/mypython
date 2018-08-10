import re
from datetime import datetime, date, time
import math

def to_pacific_time_zone(game_time):
    """ convert estern time to pacific time zone """
    print game_time
    (time,ampm) = game_time.split()
    (hour,min) = time.split(':')
    hour = int(hour)
    if re.search(r'pm', game_time):
       print "hour = ", hour
       hour += 12

    hour -= 3
    if hour < 12:
        ampm = "am"
    return str(hour)+":"+min+" "+ampm

game_time = "1:00 pm"
print to_pacific_time_zone(game_time)
print datetime.now()
print date.fromordinal(1)

dt = datetime.strptime("21/11/06 16:30", "%d/%m/%y %H:%M")
print dt