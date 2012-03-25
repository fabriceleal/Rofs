#!/usr/bin/python

from secret import *
from dropbox import client, rest, session
#from pprint import pprint
from pprint import pformat
from priv_logging import getLogger
from cache import Cache
from tempfile import mkstemp
import logging
import sys

# TODO: This should be a singleton class

logger = getLogger('dropbox_manager')

class DropboxManager:
	"""
	This class will be responsible fo handling calls to dropbox and for managing access tokens
	"""

	def __init__(self):
		
		self.create_session()
		self.create_access_token()

	def create_session(self):
		"""
		Create object session from the app key, secret and type
		"""
		try:
			self.session = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
		except Exception, e:
			logger.error('Exception at create_session')
			logger.debug('*' + sys.exc_info()[0])

	def create_access_token(self):
		"""
		Obtains an authorization url; After authorization, 
		creates an access token and builds an instance of the Dropbox client.
		Creates the metadata cache.
		"""
		# Wraper for also caching invalid results
                #def getMetadataRofs(path):
                #	try:
                #        	return self.client.metadata(path)
                #        except Exception, e:
                #                log.write('Exception at getMetadataRofs for path '+ path + '\n')
                #                pprint(e, log)
                #                return False

		try:
			request_token = self.session.obtain_request_token()
			url = self.session.build_authorize_url(request_token)
			print url
			raw_input()
			access_token = self.session.obtain_access_token(request_token)
			self.client = client.DropboxClient(self.session)
			
			# Build cache for metadata querying

			# Wraper for also caching invalid results
			def getMetadataRofs(path):
				try:
					return self.client.metadata(path)
				except Exception, e:
					logger.error('Exception at getMetadataRofs for path '+ path + '\n')
		                        logger.debug(sys.exc_info()[0])
					return False

			self.cache_metadata = Cache(getMetadataRofs)
			self.cache_files = {}

		except Exception, e:
			logger.error('Exception %s at create_access_token' % (sys.exc_info()[0]))
			logger.debug(pformat(sys.exc_info()))

	def getMetadata(self, path):
		try:
			#folder_metadata = self.client.metadata(path)
			folder_metadata = self.cache_metadata.getValue(path)

			logger.info( "Metadata for " + path)
			logger.info( pformat(folder_metadata))
			return folder_metadata
		except Exception, e:
			logger.error('Exception %s at getMetadata for path %s' % (sys.exc_info()[0], path))
			logger.debug(pprint(sys.exc_info()))
			return False

	def getFile(self, path):
		"""
		Returns the name of the generated temp file
		"""
		try:
			logger.info('getFile(%s)' % (path))

			# Check if file is in cache
			if self.cache_files.has_key(path):
				logger.info('* Retrieving tmpfile name from the cache')
				return self.cache_files[path]['tmpfile']
			else:
				logger.info('* Needs to download the file')

				# Generate temp file
				tmp, tmp_name = mkstemp()
				logger.info('* Generated name = %s' % (tmp_name))

				# Download file from dropbox
				if self.downloadFile(path, tmp) == True:
					logger.info('* File downloaded')

					# Add to cache
					self.cache_files[path]['tmpfile'] = tmp_name
					logger.info('* Added to cache')
				else:
					return False

				return tmp_name
		except Exception, e:
			logger.error("Exception %s at getFile(%s)" % (sys.exc_info()[0],path))
			logger.debug(pformat(sys.exc_info()))
			return False

	def downloadFile(self, path, out):
		try:

			# Downloads from dropbox
			# Manually :( update the metadata cache
			f, metadata = client.get_file_and_metadata(path).read()
			self.cache_metadata.setNewValue(path, metadata)
			# Write to tmp file and close
			out.write(f)
			out.close()
		
			return True
		except Exception, e:
			logger.error("Exception %s at downloadFile(%s)" % (sys.exc_info()[0], path))
			logger.debug(pformat(sys.exc_info()))
			return False

