#!/usr/bin/python


from cache import Cache, CacheFunctional
from time import sleep
from pprint import pprint

def func(x):
	sleep(5)
	return x*x

c = Cache(func)
pprint(c)
print "The 1st access should take seconds, the second one should be instantaneous."

print "1st Access = ", c.getValue(5)
print "2nd Access = ", c.getValue(5)

def fibo(fact):
	def body(n):
		if n in [0, 1]:
			return n
		else:
			return fact(n-1)+fact(n-2)
	return body


cf = CacheFunctional(fibo)

print "If the next test is not instantaneous, you better 'Ctrl-C' this; the universe will end sooner than this calculation"

print "fibo(100) = ", cf.getValue(100)
