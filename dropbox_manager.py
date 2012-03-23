#!/usr/bin/python

from secret import *
from dropbox import client, rest, session
from pprint import pprint

# TODO: This should be a singleton class

class DropboxManager:
	"""
	This class will be responsible fo handling calls to dropbox and for managing access tokens
	"""

	def __init__(self):
		self.create_session()
		self.create_access_token()

	def create_session(self):
		self.session = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)

	def create_access_token(self):
		request_token = self.session.obtain_request_token()
		url = self.session.build_authorize_url(request_token)
		print url
		raw_input()
		access_token = self.session.obtain_access_token(request_token)
		self.client = client.DropboxClient(self.session)

	def getMetadata(self, path):
		folder_metadata = self.client.metadata(path)
		print "Metadata for ", path
		pprint(folder_metadata)
		return folder_metada

	def downloadFile(self, path, destiny):
		out = open(destiny, 'w')
		f, metadata = client.get_file_and_metadata(path).read()
		out.write(f)

