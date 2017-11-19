#!/usr/bin/env python2
import random
import wurstApiClient

client = wurstApiClient.DbClient("twitterprinter", "http://151.217.83.30:5000")

client.addPubMethod("twitterprinter")

s = client.getEan(1)

with open('/dev/lp0', "w") as lp:
    lp.write("\r\n\x1D\x6B\x00{}\x00".format(s))
    lp.write("\r\n{}\r\n\r\n\r\n".format(s))
    lp.write("\x1dV\x01")	# Paper Cut


