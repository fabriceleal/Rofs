

from secret import *



#print TEST_SECRET

from dropbox import client, rest, session

sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)

request_token = sess.obtain_request_token()

url = sess.build_authorize_url(request_token)

print url
raw_input()

access_token = sess.obtain_access_token(request_token)

client = client.DropboxClient(sess)


