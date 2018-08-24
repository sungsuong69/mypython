import urllib
try:
    x = urllib.urlopen("http://www.picknpull.com/")
    #print(x.read())
except Exception as e:
    print(str(e))

# Make soup
try:
    ncaaf_resp = urllib.urlopen("http://www.picknpull.com/")
    #resp = urllib.urlopen("http://www.donbest.com/ncaaf/odds/")
except URLError as e:
    print 'An error occured fetching %s \n %s' % (url, e.reason)   

resp = ncaaf_resp + nfl_resp
soup = BeautifulSoup(resp.read(),features="html.parser")

# Get table
try:
    tables = soup.find_all('table')
except AttributeError as e:
    print 'No tables found, exiting'
   
#print x.read()