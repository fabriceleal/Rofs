import logging

FORMAT = "%(levelno)-5s %(asctime)-15s %(message)s"

def getLogger(name, filename = None, level = logging.INFO):
	"""
	Create logger object, adding a FileHandler.
	"""
	try:
		if filename == None or filename == '':
			filename = name + '.log'

		logger = logging.getLogger(name)
		logger.setLevel(level)
		handler = logging.FileHandler(filename)
		handler.setFormatter(logging.Formatter(FORMAT))
		logger.addHandler(handler)
		return logger
	except Exception, e:
		print "Exception generating logger for %s, file %s, level %s, format %s" % (name, filename, level, FORMAT)
