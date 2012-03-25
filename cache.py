#!/usr/bin/python
from time import time
import logging
from priv_logging import getLogger

logger = getLogger('cache')

def y(function):
	"""
Based in the javascript implemention at http://matt.might.net/articles/implementation-of-recursive-fixed-point-y-combinator-in-javascript-for-memoization/

The Y combinator finds the fixed point of the "functional" passed in as an argument.
Thus, the Y combinator satisfies the property:
	Y(F) = F(Y(F))

Usage:
	(Factorial example)
	> factgen = lambda fact: lambda x: ((x == 0 and 1) or (x * fact(x-1)))
	> (y(factgen))(6)
	720
	
	"""
	return (lambda x: function(lambda y: (x(x))(y) )) (lambda x: function(lambda y: (x(x))(y)  ) )



	
def y_mem_body(cache, arg):
	"""
Implementation of the memoization technique using the y-combinator, based in the javascript implementation at http://matt.might.net/articles/implementation-of-recursive-fixed-point-y-combinator-in-javascript-for-memoization/
	"""
	if cache.checkValidity(arg):
		logger.info('get ' +str(arg)+' from store')

		cache.updateStat(args)

		return cache.cache[arg]['value'] # Do not use getValue() !
	else:
		logger.info('calculate ' + str(arg))

		# Execute function
		result = (cache.functional( cache.y ))(arg)

		# Cache and return result
		cache.setNewValue(result)
		
		return result	



# TODO: This should be abstract
class CacheBase:
	def __init__ (self, functional):
		self.cache = {}
		self.functional = functional
		self.y = self.getYMemorizable()

        def checkValidity(self, arg):
                """
                Simple implementation. Returns true if the element is in the cache; otherwise, returns False.

                Returns: True to retrive from cache, false to (re)calculate
                """

                if self.cache.has_key(arg):
                        return True
                return False


        def getValue(self, arg):
		"""
		Retrieves a value from the cache; if the value is not yet in the cache, 
		executes the y-combinator with memoization of the supplied functional.
		"""
                return self.y(arg)

        def getYMemorizable(self):
		"""
		Retrieves the y-combinator with memoization of the supplied functional.
		"""
                return lambda arg: y_mem_body(self, arg)
	
	def setNewValue(self, arg, value):
		"""
		Inserts a value in the cache.
		"""
		self.cache[arg] = { 'value' : result, 'reads' : 1, 'last' : time() }
	
	def updateStat(self, arg):
		"""
		Updates stats of a value in the cache.
		"""
		self.cache[arg]['reads'] = cache.cache[arg]['reads'] + 1
                self.cache[arg]['last']  = time()



class CacheFunctional(CacheBase):

	def __init__(self, functional):
		CacheBase.__init__(self, functional)



class Cache(CacheBase):
	"""
Proxy that caches results for one function. 
You don't have to touch in your function! ;)

Usage: 
	c = Cache(lambda x: x+x)
	t = c.getValue(3)
	t = c.getValue(3)
	
	"""
	def __init__(self, function):
		CacheBase.__init__(self, lambda funct : lambda n: function(n))
		# self.function = function



