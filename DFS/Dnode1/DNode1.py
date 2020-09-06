# -*- coding: utf-8 -*-
"""

=================== DATA NODE 1 ===================

IP,PORT,PATH = "127.0.0.1",8888,r'C:\Temp\TMP\DFS\Dnode1'


FTP: file -> ftpserver2.py || port: 8889  (Dnode port + 1)
    Usrname: ftpuser || password: pass

===================================================

"""
import os, rpyc, subprocess
from datetime import  datetime as dt
from rpyc.utils.server import ThreadedServer
from rpyc.lib import setup_logger

global IP,PORT,PATH
IP,PORT,PATH = "127.0.0.1",8888,r'C:\Temp\TMP\DFS\Dnode1'
timeformat = "%Y-%m-%d %H:%M:%S"                        # Used to print Modified time for files

class DNServer(rpyc.Service):
    class exposed_DNode():

        @staticmethod
        def exposed_filequery():
            print (PATH)
            filelist = []                                       # Create a null file list to append data while iterating
            for (dirpath, dirnames, filename) in os.walk(PATH): # iterating through each folder/ file in PATH
                for file in filename:
                    tempdict = {}                               # Creating a temporary dictionary to record file attributes
                    tempdict['DN_IP'] = IP                      # Assigning values for current file to th temp dict
                    tempdict['DN_Port']  =PORT
                    tempdict['Location'] = dirpath
                    tempdict['Name'] = file
                    tempdict['Size'] = os.path.getsize(os.path.join(dirpath,file))          # need to specify full path+filename to get the filesize as only filename is not recognized
                    mtime = dt.fromtimestamp(os.path.getmtime(os.path.join(dirpath,file)))  # This returns a datetime object datetime.datetime(YYYY, MM, DD, hh, mm, ss, ms)
                    tempdict['ModTime'] = mtime.strftime(timeformat)                        # Formats the mtime to "YYYY-MM-DD hh:mm:ss" which is human readable
                    filelist.append(tempdict)                           # Appends each file to the filelist
            print (filelist)
            return (filelist)

if __name__ == "__main__":
    t1 = ThreadedServer(DNServer, hostname=IP, port=PORT, protocol_config={'allow_public_attrs': True})
                                                # 'allow_public_attrs' is needed to make the rpyc items visible. If this is not specified, it will result in errors
                                                # .. since rpyc dicts & lists are not visible as normal dict and list 
                                                # e.g. while converting an rpyc list of dict (filelist) to dataframe, it returns 'keys' error
    setup_logger(quiet=False, logfile=None)
    subprocess.call("start cmd /K python ftpserver1.py", shell=True) # this opens the ftpserver1.py file in a new console window (shell=True) so that we can view the FTP logs
    t1.start()                                  # Start the DNode server

""" NOTE:
Here we call the ftpserver script separately as including teh FTP script in this file 
creates collision between the rpyc logging and ftp logging & it was difficult to run both simultaneously
USing a new window for FTPserver fixes this issue
"""