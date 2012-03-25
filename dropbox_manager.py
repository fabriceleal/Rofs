#!/usr/bin/python

from secret import *
from dropbox import client, rest, session
#from pprint import pprint
from pprint import pformat
from priv_logging import getLogger
from cache import Cache
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
		try:
			self.session = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
		except Exception, e:
			logger.error('Exception at create_session')
			logger.debug('*' + sys.exc_info()[0])

	def create_access_token(self):
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

		except Exception, e:
			logger.error('Exception at create_access_token\n')
			logger.debug(sys.exc_info()[0])

	def getMetadata(self, path):
		try:
			#folder_metadata = self.client.metadata(path)
			folder_metadata = self.cache_metadata.getValue(path)

			logger.info( "Metadata for " + path)
			logger.info( pformat(folder_metadata))
			return folder_metadata
		except Exception, e:
			logger.error('Exception at getMetadata for path '+ path)
			logger.debug(sys.exc_info()[0])
			return False

	def downloadFile(self, path, destiny):
		out = open(destiny, 'w')
		f, metadata = client.get_file_and_metadata(path).read()
		out.write(f)

