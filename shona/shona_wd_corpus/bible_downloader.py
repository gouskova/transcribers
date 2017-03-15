#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#never got this working, the bible.com pages are full of garbage
#Downloads the Shona bible files from bible.com


import urllib
from urllib.parse import urlparse
import re, os

bibdir = os.getcwd()+'/biblefiles/'

if not bibdir.isdir():
    os.mkdir(bibdir)

linkre = re.compile(r'.*?.bdmcs')

biblink = urllib.urlopen('https://www.bible.com/bible/32/jhn.1').read()

for link in linkre.findall(biblink):
	
	split = urlparse.urlsplit(link)
	filename = biblink + split.path.split("/")[-1]
	#print filename
	urllib.urlretrieve(link, filename)
	
	print('downloaded ' + link)


print ('done downloading')

