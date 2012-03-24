#!/usr/bin/python


from cache import *
from time import *


def func(x):
	sleep(5)
	return x*x

c = Cache(func)

print "The 1st access should take seconds, the second one should be instantaneous."

print "1st Access = ", c.getValue(5)
print "2nd Access = ", c.getValue(5)



