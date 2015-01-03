#!/usr/bin/python2

# This scripts fetches tweets from twitter and outputs them text-based to a TCP-socket.
# It also appends "cut" instructions for endless-paper cash register receipt printers.
# The TCP-Socket can be hosted on a simple old-fashioned Print-Server.
#
# Needs python-twitter
# https://github.com/bear/python-twitter
# apt-get install python-twitter
#
# Line-Feeds are optimized for CBM-1000 https://stratum0.org/wiki/CBM_1000

import twitter
import time
import sys
import HTMLParser
import os
import config
import socket


# Make some stuff to fetch config
consumer_key=config.consumer_key
consumer_secret=config.consumer_secret
access_token_key=config.access_token_key
access_token_secret=config.access_token_secret


# Prints a status st to a given socket s
def pst(st,f):
	h = HTMLParser.HTMLParser()
	f.send(h.unescape("@"+st.user.name.encode('ascii', 'ignore'))+"\r\n")
	f.send(str(st.created_at)+"\r\n")
	f.send(st.text.encode('ascii', 'ignore')+"\r\n\r\n\r\n\r\n")
	f.send("\x1dV\x01")	# Paper Cut

# Searches twitter and prints all statuses, that are new
def get(ids,term, api,f):
	s = api.GetSearch(term)
	for st in s:
		if st.id not in ids:
			pst(st,f)
			ids.append(st.id)

# Seaches twitter and marks all found tweets as old
def init(ids,term, api):
	s = api.GetSearch(term)
	for st in s:
		ids.append(st.id)


api = twitter.Api(consumer_key, consumer_secret, access_token_key, access_token_secret)

ids = []

#terms = ["mensadisplay", "stratum0", "#ungestreamt"]
terms = config.terms

print "Twitter that shit!"
print "@@@@@@@@@@@@@@@@@@"
print ""

for t in terms:
	init(ids, t, api)

while 1:
	print "."
	f = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	f.connect((config.ip_addr,config.tcp_port))
	for t in terms:
		get(ids, t, api,f)
	f.close()

	time.sleep(20)
