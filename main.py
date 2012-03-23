#!/usr/bin/python

from secret import *
from pprint import pprint

#print TEST_SECRET

from dropbox import client, rest, session

sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)

request_token = sess.obtain_request_token()

url = sess.build_authorize_url(request_token)

print url
raw_input()

access_token = sess.obtain_access_token(request_token)

client = client.DropboxClient(sess)

print "linked account:" 
pprint(client.account_info())

folder_metadata = client.metadata('/')

print "metadata:" 
pprint(folder_metadata)

if folder_metadata['is_dir'] == True:
	print "isdir"
else:
	print "ko"

for folder in map(lambda n : n['path'][1:] , client.metadata('/')['contents']):
	print folder


