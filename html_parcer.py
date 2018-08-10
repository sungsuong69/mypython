from HTMLParser import HTMLParser
import urllib

class MyHTMLParser(HTMLParser):

   #Initializing lists
   lsStartTags = list()
   lsEndTags = list()
   lsStartEndTags = list()
   lsComments = list()

   #HTML Parser Methods
   def handle_starttag(self, startTag, attrs):
       self.lsStartTags.append(startTag)
       for attr in attrs:
            print "     attr:", attr

   def handle_endtag(self, endTag):
       self.lsEndTags.append(endTag)

   def handle_startendtag(self,startendTag, attrs):
       self.lsStartEndTags.append(startendTag)

   def handle_comment(self,data):
       self.lsComments.append(data)


#creating an object of the overridden class
parser = MyHTMLParser()

#Opening NYTimes site using urllib2
html_page = urllib.urlopen("http://www.donbest.com/nfl/odds/")

#Feeding the content
parser.feed(str(html_page.read()))

print "hello"
print ("start_tag", parser.lsStartTags)
print ("end_tag", parser.lsEndTags)
print ("comment_tag",parser.lsComments)