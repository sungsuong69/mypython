import re
D = {'Composer 10:00 pm': {'first': 'Johannes', 'last' : 'Brahms'},
     'Composer 1:00 am': 'Romantic',
     'composer 8:00 pm' : ['Piano Concerto No. 1', 'Piano Concerto No. 2', 'Symphony No. 1', 'Symphony No. 2', 'Violin Concerto in D Major', 'Hungarian Dances'] }

#print D['Composer']

string = "pk"
#print float(string)

def mysort(elem):
    print elem
    (string,time) = elem.split()
    (hour,min) = time.split(':')
    return int(hour)

#----------------------------------------------------------------------
def mysortbytime(elem):
#----------------------------------------------------------------------
    """taking elem as datetime as (dayofweek,month,dayofmonth,time,ampm) = elem.split() """
    (string,time,ampm) = elem.split()
    civilian_time = time + " " + ampm
    (hour,min) = to_military_time(civilian_time).split(':')
    return int(hour)
#----------------------------------------------------------------------
def to_military_time(civilian_time):
#----------------------------------------------------------------------
    (time,ampm) = civilian_time.split()
    (hour,min) = time.split(':')
    if re.search(r'PM',civilian_time):
       hour += 12 
    return hour + ":" + min 

print sorted(D,key=mysortbytime)