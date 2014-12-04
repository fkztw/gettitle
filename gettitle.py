#!/usr/bin/env python2

import urllib2
import sys
from bs4 import BeautifulSoup as bs

url  = str(sys.argv[1])
soup = bs(urllib2.urlopen(url))

print
print soup.title.string
print url
print