Rofs
====

Dropbox ReadOnly FileSystem
---------------------------

*nix mountable filesystem implemented using the Dropbox Python SDK and the Python binding for FUSE. Data (dir / file metadata and files` content) is downloaded on-demand and cached on the local machine, so the first time you open a file or ls a dir you may have to wait a while :(

There isn't yet any heurestics for droping old cached values, so, as for now, the first response of Dropbox for any query (metadata or file content) will be the one that you'll have until you umount the filesystem :P

This filesystem is not 100% POSIX compliant, so do not expect much. 


Using
------------
You'll have to install the Python binding for FUSE. For now I'm excluding the file with the app key, secret and type of the git repository, for obvious reasons. 
And you must install the Dropbox Python SDK.

Usage
-----
Use `mount.sh` to mount the file system, `clean.sh` removes log files and .pyc files, and `umount.sh` unmounts the filesystem
