__author__ = 'illuminati'
import urllib
params = urllib.urlencode({"username":"ajinkya", "type":"admin"})
print urllib.urlopen("http://127.0.0.1:5000/lock",params).read()
print urllib.urlopen("http://127.0.0.1:5000/open",params).read()
print urllib.urlopen("http://127.0.0.1:5000/open",params).read()