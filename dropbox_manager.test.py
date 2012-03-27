#!/usr/bin/python

from dropbox_manager import DropboxManager


d = DropboxManager()


path = '/Livros/perl/utf8.pdf'

metadata = d.client.metadata(path)

if metadata == None:
	print "Error getting metadata for file %s" % path
else:
	print metadata

f = d.getFile(path)

if f == False:
	print "Error downloading file %s" % path
else:
	fo = None
	try:
		fo = open(f, 'r')
		print "Everything seems ok with file %s" % path
	except:
		print "Error opening file %s" % path
	finally:
		if fo != None:
			fo.close()

