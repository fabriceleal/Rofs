#!/usr/bin/python

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
	return (lambda(x) : function( lambda(y) : (x(x))(y) )) ( lambda(x) : function( lambda(y) : (x(x))(y)  ) )
	
def y_mem_body(cache, arg):
	if cache.checkValidity(arg):
		# Update reading stats, return stored value
		cache.cache[arg]['reads'] = cache.cache[arg]['reads'] + 1
		cache.cache[arg]['last']  = None
		return cache.cache[arg]['value']
	else:
		# Execute function
		result = (cache.functional( cache.y ))(arg)
		# Cache and return result
		cache.cache[arg] = { 'value' : result, 'reads' : 1, 'last' : None  }
		
		return result	
	
class CacheFunctional:
	def __init__(self, functional):
		pass
# TODO: Make version that accepts a functional, to allow memoization of recursive functions.	
	

class Cache:
	"""
Proxy that caches results for one function. 
You don't have to touch in your function! ;)

Usage: 
	c = Cache(lambda x: x+x)
	t = c.getValue(3)
	t = c.getValue(3)
	
	"""
	def __init__(self, function):
		self.cache = {}
		self.function = function
		self.functional = lambda funct : lambda n : function(n)
		self.y = self.getYMemorizable()
	
	def checkValidity(self, arg):
		"""
		Simple implementation. Returns true if the element is in the cache; otherwise, returns False.

		Returns: True to retrive from cache, false to (re)calculate
		"""
				
		if self.cache.has_key(arg) != None:
			return True
		return False		
		

	def getValue(self, arg):
		return self.y(arg)

	def getYMemorizable(self):
		return lambda arg: y_mem_body(self, arg)


