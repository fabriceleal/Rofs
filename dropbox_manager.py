#!/usr/bin/python

from secret import *
from dropbox import client, rest, session
from pprint import pprint

# TODO: This should be a singleton class

log = open('/home/user/dropmngr', 'w', False)

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
			log.write('Exception at create_session\n')
			pprint(e, log)

	def create_access_token(self):
		try:
			request_token = self.session.obtain_request_token()
			url = self.session.build_authorize_url(request_token)
			print url
			raw_input()
			access_token = self.session.obtain_access_token(request_token)
			self.client = client.DropboxClient(self.session)
		except Exception, e:
			log.write('Exception at create_access_token\n')
			pprint(e, log)

	def getMetadata(self, path):
		try:
			folder_metadata = self.client.metadata(path)
			log.write( "Metadata for " + path + '\n')
			pprint(folder_metadata, log)
			return folder_metadata
		except Exception, e:
			log.write('Exception at getMetadata for path '+ path + '\n')
			pprint(e, log)
			return False

	def downloadFile(self, path, destiny):
		out = open(destiny, 'w')
		f, metadata = client.get_file_and_metadata(path).read()
		out.write(f)
