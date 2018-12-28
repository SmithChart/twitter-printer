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
if config.wurstEnable:
    import wurstApiClient


# Make some stuff to fetch config
consumer_key=config.consumer_key
consumer_secret=config.consumer_secret
access_token_key=config.access_token_key
access_token_secret=config.access_token_secret


# Prints a status st to a given socket s
def pst(st):
        global wurst
        global lastWurst
	h = HTMLParser.HTMLParser()
	lpr(h.unescape("@"+st.user.screen_name.encode('latin1', 'ignore'))+"\r\n")
	lpr(str(st.created_at)+"\r\n")
	lpr(st.text.encode('latin1', 'ignore')+"\r\n\r\n\r\n\r\n")
        if config.wurstEnable:
            if config.wurstKeyword.lower() in st.text.lower():
                if (float(time.time()) - lastWurst) > config.wurstTimeout:
                    lpr("Here is your free wurstcher:\r\n")
                    code = int(wurst.getEan(1))
                    lpr("\x1D\x6B\x00{:011}\x00".format(code))
                    lpr("\r\nGo to Freiwurst to obtain your free Wurst")
                    lpr("\r\n\r\n\r\n\r\n")
                    lastWurst = float(time.time())
                else:
                    lpr("Sorry you can only generate one wurtcher every minute :(\r\n")
                    lpr("\r\n\r\n\r\n\r\n")
	lpr("\x1dV\x01")	# Paper Cut

# Searches twitter and prints all statuses, that are new
def get(ids,term, api):
	s = api.GetSearch(term +" -RT")
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
        global numtweets

	print s
        
        numtweets = numtweets + 1 

	if sock is not None:
		sock.send(s)
	
	if port is not None:
		port.write(s)
                time.sleep(0.1) # TODO: fix tis later


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

i = 0

numtweets = 0

counttostat = 0


if config.wurstEnable:
    # prepare the freiwurstClient
    wurst = wurstApiClient.DbClient("twitterprinter", config.wurstDbHost) 
    wurst.addPubMethod(config.wurstPubMethod)
    lastWurst = float(time.time())-config.wurstTimeout*2

while True:
    #reload ads
    ads = []
    adsdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), config.ads)
    for file in os.listdir(adsdir):
        with open(os.path.join(adsdir, file), 'r') as f:
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


