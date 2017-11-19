#!/usr/bin/python2

# Twitter API Credentials
consumer_key='gzluruR16vujcXYzDRYstsaZo'
consumer_secret='ExnNgMcxhd4f0S9vSXbk5VnMjjWZ7vqVhrDp4T5UP3HTTILNRR'
access_token_key='604747216-XZjAPAoGoeHb1caGnanFWwR2HQLCpeoTGzlsBzFC'
access_token_secret='F8Mxi8NbHoqjJ4FezeejLq5HkRkPSvPff5yGIbJYWPNDb'

# Twitter seach Terms
terms = ["#DudW", "Sonntag", "ist"]

# TCP/IP Settings of print-Server
#ip_addr = '192.168.178.226'
#tcp_port = 9100

# path of lpr
lpr = '/dev/lp0'


# ads 
# all files in this dir will be treated as ads and be randomly chosen.
ads = './ads/'
# ads will be inserted every n tweets
adsn = 20
# ast least one ad will be inserted every cycle
forceadd = False

#wurstcher Config
#this enanbles you to print wurstchers \o/
wurstEnable = False# activate this to activate wurstSupport
wurstDbHost = "http://151.217.83.30:5000"
wurstPubMethod = "twitterprinter"
wurstTimeout = 60.0 # minimum time between two wurstchers in [s]
wurstKeyword = "freiwurst"

