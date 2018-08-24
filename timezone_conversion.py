import re
from datetime import datetime
from datetime import date
import math

import time
from datetime import date
#from datetime import time
today = date.today()
print today

print date(2018, 8, 13).isoweekday()

print time.clock()
print time.gmtime()
print time.localtime()
localtime = time.localtime()
(year,month,mday,hour,min,sec,wday,yday,isdst) = localtime
t = (year, month, mday, hour, min, sec, wday, yday, 0)
secs = time.mktime( t )
print "time.mktime(t) : %f" %  secs
print "asctime(localtime(secs)): %s" % time.asctime(time.localtime(secs))

print time.localtime(secs)

t = (year, month, mday, hour, min, sec, wday, yday, 1)
secs = time.mktime( t )

print "time.mktime(t) : %f" %  secs
print "asctime(localtime(secs)): %s" % time.asctime(time.localtime(secs))

print time.localtime(secs)

t = (year, month, mday, hour, min, sec, wday, yday, -1)
secs = time.mktime( t )
print "time.mktime(t) : %f" %  secs
print "asctime(localtime(secs)): %s" % time.asctime(time.localtime(secs))

print time.localtime(secs)

secs -= (3600*3)
print time.localtime(secs)

#now = int(time.time())
#print "now = ", now

    
#after1000 = int(time.time())
#print "after1000 = ", after1000

#print datetime.time()

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
#print date.isoweekday()
print date.fromordinal(1)

dt = datetime.strptime("21/11/06 16:30", "%d/%m/%y %H:%M")
print dt