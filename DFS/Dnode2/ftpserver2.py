# -*- coding: utf-8 -*-
"""
============ FTP Server 2 (for DNode2) ============

root directory: r'C:\Temp\TMP\DFS\Dnode2'


FTP: Host: '127.0.0.1' || port: 8001  (Dnode port + 1)
    Usrname: ftpuser || password: pass

===================================================
"""

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer
                                                # Threaded server is used to enable multiple ftp threads for different users

host = '127.0.0.1'
port = 8001                                     # DNode port is 8888; FTP port is the next port 8888+1

def main():
    authorizer = DummyAuthorizer()
    authorizer.add_user('ftpuser', 'pass', homedir=r'C:\Temp\TMP\DFS\Dnode2', perm='elradfmw') # set username, password & homedirectory for the user
    handler = FTPHandler
    handler.authorizer = authorizer
    server = ThreadedFTPServer((host,port), handler)                      # Bind the host:port for FTP services  
    print ("Starting FTP Server on port:",port)
    server.serve_forever()                                  # Start FTP server
    
def stopftp():
    print ("Stopping FTP Server on port:",port)
    main.server.close_all()                                 # Close all instances (Threads) of the ftp server-client connections


if __name__ == "__main__":
    main()