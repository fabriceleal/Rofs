#!/usr/bin/python

import fuse
from pprint import pformat
import logging
from priv_logging import getLogger
from fuse import Fuse
from dropbox_manager import DropboxManager
from time import time

import stat    # for file properties
import os      # for filesystem modes (O_RDONLY, etc)
import errno   # for error number codes (ENOENT, etc)
               # - note: these must be returned as negatives

# TODO: Check if fuse has attribute __version__

fuse.fuse_python_api = (0, 2)

logger = getLogger('rofs_fuse')

manager = DropboxManager()

def dirFromList(list):
    """
    Return a properly formatted list of items suitable to a directory listing.
    [['a', 'b', 'c']] => [[('a', 0), ('b', 0), ('c', 0)]]
    """
    return [[(x, 0) for x in list]]

def getDepth(path):
    """
    Return the depth of a given path, zero-based from root ('/')
    """
    if path == '/':
        return 0
    else:
        return path.count('/')

def getParts(path):
    """
    Return the slash-separated parts of a given path as a list
    """
    if path == '/':
        return [['/']]
    else:
        return path.split('/')

class RofsStat(fuse.Stat):
	"""
	"""
	
	def __init__(self):
		self.st_mode  = 0;
		self.st_ino   = 0;
		self.st_dev   = 0;
		self.st_nlink = 0;
		self.st_uid   = 0;
		self.st_gid   = 0;
		self.st_size  = 0;
		self.st_atime = 0;
		self.st_mtime = 0;
		self.st_ctime = 0;

class RofsFuse(Fuse):
    """
    """
    
    def __init__(self, *args, **kw):
        Fuse.__init__(self, *args, **kw)

	logger.info('Init complete')
        print 'Init complete.'

    def getattr(self, path):
        """
        - st_mode (protection bits)
        - st_ino (inode number)
        - st_dev (device)
        - st_nlink (number of hard links)
        - st_uid (user ID of owner)
        - st_gid (group ID of owner)
        - st_size (size of file, in bytes)
        - st_atime (time of most recent access)
        - st_mtime (time of most recent content modification)
        - st_ctime (platform dependent; time of most recent metadata change on Unix,
                    or the time of creation on Windows).
        """
	try:
	        logger.info('getattr')

        	#depth = getDepth(path) # depth of path, zero-based from root
	        #pathparts = getParts(path) # the actual parts of the path
        	#return -errno.ENOSYS

		st = RofsStat()
	
		logger.info('Looking for metadata of %s' % (path))

		metadata = manager.getMetadata(path)

		logger.info('* Data = %s' % (pformat(metadata)))

		if metadata != False:
			logger.info('* Has metadata')
			if metadata['is_dir'] == True:
				logger.info('** Is dir')
				st.st_mode  = stat.S_IFDIR | 0755
				st.st_nlink = 2
			else:
				logger.info('** Is file')
				st.st_mode  = stat.S_IFREG | 0444
				st.st_nlink = 1
								 
				st.st_size  = int(metadata['bytes'])
		else:
			logger.info('* No metadata found')
			return -errno.ENOENT

		return st
	except Exception, e:
		logger.error('Exception at getattr')
		logger.debug(pformat(sys.exc_info()))
		return -errno.ENOSYS

    def readdir(self, path, offset):
	all_folder = ['.', '..']

	try:
		logger.info('readdir(\'%s\', %d)' % (path, offset))
	
		metadata = manager.getMetadata(path)

		#if metadata == False:
		#	return -errno.NOENT
	
		all_folder = ['.', '..']

		if metadata != False:
			logger.info('* %s has metadata.' % (path))
			#for elem in metadata['contents']:
			#	logger.info("** subitem '%s'" % (elem['path']))
			
			# Dropbox always returns full paths, '/'-based. 
			# readir's path always has a full path, '/'-based
			# remove readir's path from the dropbox returned dir name

			# TODO: Very very very ugly
			
			offset = len(path)
			if path[-1] != '/':
				offset = offset + 1

			all_folder = all_folder + map(lambda n : n['path'][offset:] , metadata['contents'])			
		
	except Exception, e:
		logger.error("Exception %s in readdir." % (sys.exc_info()[0]))
		logger.debug(pformat(sys.exc_info()))

	for folder in all_folder:
		logger.info('* yielding at %s for %s' % (path, folder))
		yield fuse.Direntry(folder)



    def getdir(self, path):
        """
        return: [[('file1', 0), ('file2', 0), ... ]]
        """
	try:
        	logger.info('getdir(%s)' % path)
	except:
		pass
        return -errno.ENOSYS

    def mythread ( self ):
        logger.info('*** mythread')
        return -errno.ENOSYS

    def chmod ( self, path, mode ):
        logger.info("*** chmod ('%s', %s)" % (path, oct(mode)))
        return -errno.ENOSYS

    def chown ( self, path, uid, gid ):
        logger.info("*** chown ('%s', %d, %d)" % (path, uid, gid))
        return -errno.ENOSYS

    def fsync ( self, path, isFsyncFile ):
        logger.info("*** fsync ('%s', %d)" % (path, isFsyncFile))
        return -errno.ENOSYS

    def link ( self, targetPath, linkPath ):
        logger.info("*** link ('%s', '%s')" % (targetPath, linkPath))
        return -errno.ENOSYS

    def mkdir ( self, path, mode ):
        logger.info("*** mkdir ('%s', %s)" % (path, oct(mode)))
        return -errno.ENOSYS

    def mknod ( self, path, mode, dev ):
        logger.info("*** mknod ('%s', %s, %d)" % (path, oct(mode), dev))
        return -errno.ENOSYS
	
    def open ( self, path, flags ):
	"""
	Open directory
	"""
	# TODO: confirm this

	try:        
		logger.info('open(%s, %d)' % (path, flags))

        	# TODO: Validate path, on error return -errno.ENOENT

			
		accmode = os.O_RDONLY | os.O_WRONLY | os.O_RDWR
		if (flags & accmode) != os.O_RDONLY:
			return -errno.EACCES
        
        except Exception, e:
                logger.error('Exception at open (%s, ...)' % path)
                logger.debug(pformat(sys.exc_info()))
		return -errno.ENOSYS

	# Otherwise, return without error...


    def read ( self, path, length, offset ):
	try:

	        logger.info('read (%s, %d, %d)' % (path, length, offset))
		
		fname = manager.getFile(path)
		logger.info('* got file, is at %s' % fname)
			
		if fname == False:
			logger.info('* read is going to return NOENT ...')
			return -errno.NOENT # TODO: confirm
		else:
			logger.info('* about to open file %s' % fname)
			# Read and return from the file
			f = open(fname, 'rb')
			logger.info('* file %s opened in read+binary mode' % path)
			buf = []
			try:
				f.seek(offset)
				logger.info('* jumped to offset %d' % offset)
				buf = f.read(length)
				logger.info('* read %d bytes' % length)
			except:
				raise # TODO: Rethrow
			finally:
				f.close()
			logger.info('* returning buf with length %d' % len(buf))
			return buf

	except Exception, e:
		logger.error("Exception %s at read('%s', %d, %d)" % (sys.exc_info()[0], path, length, offset))

        return -errno.ENOSYS

    def readlink ( self, path ):
        logger.info ("*** readlink ('%s')" % path)
        return -errno.ENOSYS

    def release ( self, path, flags ):
        logger.info("*** release ('%s', %d)" % (path, flags))
        return -errno.ENOSYS

    def rename ( self, oldPath, newPath ):
        logger.info("*** rename ('%s', '%s')" % (oldPath, newPath))
        return -errno.ENOSYS

    def rmdir ( self, path ):
        logger.info("*** rmdir ('%s')" % path)
        return -errno.ENOSYS

    def statfs ( self ):
        logger.info('*** statfs')
        return -errno.ENOSYS

    def symlink ( self, targetPath, linkPath ):
        logger.info("*** symlink ('%s', '%s')" % (targetPath, linkPath))
        return -errno.ENOSYS

    def truncate ( self, path, size ):
 	logger.info("*** truncate ('%s', %d)" % (path, size))
        return -errno.ENOSYS

    def unlink ( self, path ):
        logger.info( "*** unlink ('%s')" % (path))
        return -errno.ENOSYS

    def utime ( self, path, times ):
        logger.info( "*** utime ('%s', %d)" % (path, times))
        return -errno.ENOSYS

    def write ( self, path, buf, offset ):
	try:
	        logger.info("write ('%s', buf, %d)" % (path, offset))
        except:	
		pass
	return -errno.ENOSYS


def main():
	usage = """

	rofs: A readonly Dropbox filesystem

	Usage: 		./rofs.py <mountpoint>
	unmount with: 	fusermount -u <mountpoint>

	"""
	fs = RofsFuse(version = "%prog " + fuse.__version__, usage=usage, dash_s_do='setsingle')
	fs.parse(errex=1)
	fs.flags = 0
	fs.multithreaded = 0
	fs.main()

if __name__ == '__main__':
	main()

