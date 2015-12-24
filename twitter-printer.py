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
import random


# Make some stuff to fetch config
consumer_key=config.consumer_key
consumer_secret=config.consumer_secret
access_token_key=config.access_token_key
access_token_secret=config.access_token_secret


# Prints a status st to a given socket s
def pst(st):
	h = HTMLParser.HTMLParser()
	lpr(h.unescape("@"+st.user.name.encode('latin1', 'ignore'))+"\r\n")
	lpr(str(st.created_at)+"\r\n")
	lpr(st.text.encode('latin1', 'ignore')+"\r\n\r\n\r\n\r\n")
	lpr("\x1dV\x01")	# Paper Cut

# Searches twitter and prints all statuses, that are new
def get(ids,term, api):
	s = api.GetSearch(term)
	for st in s:
		if st.id not in ids:
			pst(st)
			ids.append(st.id)

# Seaches twitter and marks all found tweets as old
def init(ids,term, api):
	s = api.GetSearch(term)
	for st in s:
		ids.append(st.id)

def lpr(s):
	global sock 
	global port

	print s

	if sock is not None:
		sock.write(s)
	
	if port is not None:
		port.write(s)


api = twitter.Api(consumer_key, consumer_secret, access_token_key, access_token_secret)

ids = []

terms = config.terms

print "Twitter that shit!"
print "@@@@@@@@@@@@@@@@@@"
print ""

for t in terms:
	init(ids, t, api)

sock = None
port = None


while 1:
    #reload ads
    ads = []
    for file in os.listdir(config.ads):
        with open('./ads/'+file, 'r') as f:
            ads.append(f.read())
            f.close()

    # open sockets
    if hasattr(config, 'ip_addr'):
        sock  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((config.ip_addr,config.tcp_port))

    if hasattr(config, 'lpr'):
        port = open(config.lpr, 'w')

    if sock is None and port is None:
        print "No output enabled. This is ok, but may not what you wanted. Just printing everything to screen."
    
    #output
    if config.forceadd:
        i = 0
    for t in terms:
        if (i % config.adsn) == 0:
            lpr(random.choice(ads) +"\r\n\r\n\r\n\r\n\x1dV\x01")
        i = i + 1
        get(ids, t, api)

    #cleanup
    if sock is not None:
        sock.close()

    if port is not None:
        port.close()
    
    # zZzZz
    time.sleep(20)
