#!/usr/bin/python2

from PIL import Image
import random
from bisect import bisect

def ascii(path, xs):
	greyscale = [
		" ",
		" ",
		".,-",
		"_ivc=!/|\\~",
		"gjez2]/(YL)t[+T7Vf",
		"mdK4ZGbNDXY5P*Q",
		"W8KMA",
		"#%$"
		]
		
	zonebounds=[36,72,108,144,180,216,252]

	im = Image.open(path)
	s = im.size
	print "x-Orgig:" + str(s[0])
	print "x-Soll: " + str(xs)
	ys = int((float(xs)/s[0])*s[1])
	print "y-Soll: " + str(ys)
	im = im.resize((xs, ys), Image.BILINEAR)
	im = im.convert("L")

	st = ""
	for y in range(0,im.size[1]):
		for x in range(0,im.size[0]):
			lum=255-im.getpixel((x,y))
			row=bisect(zonebounds,lum)
			possibles=greyscale[row]
			st=st+possibles[random.randint(0,len(possibles)-1)]
		st=st+"\n"

	print st


