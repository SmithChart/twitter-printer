twitter-printer
===============

This scripts fetches tweets from twitter and outputs them text-based to a TCP-socket and / or a local file (eg. your /dev/usb/lp0).

It also appends "cut" instructions for an endless-paper cash register receipt printer called CBM-1000.

The TCP-Socket can be hosted on a simple old-fashioned Print-Server or can be netcat'et to a /dev/usb/lp0.

Needs python-twitter
```
https://github.com/bear/python-twitter
apt-get install python-twitter
```
