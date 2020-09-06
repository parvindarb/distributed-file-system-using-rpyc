

DFS is the Main project folder:

Server folder contains: 
	dfs_server.py   (This is the first file to be executed. Allows user to select which port server should run on)

DNode1 folder contains:
	DNode1.py	(This is the main file to be run for DNode1 - this will automatically execute the ftpserver1.py in a new window.)
	ftpserver1.py	(No need to run this manually)
	Test1.txt   	(This is a test file used for FTP)
	test.py		(This is a test file used for FTP)

DNode2 folder contains:
	DNode2.py	(This is the main file to be run for DNode2 - this will automatically execute the ftpserver2.py in a new window.)
	ftpserver2.py	(No need to run this manually)
	Test2.txt   	(This is a test file used for FTP)

Client folder contains:
	dfs_client.py 	(This is the main client file - you can specify the master server/ port to connect to)
	ftpclient.py	(This is the hard coded ftp client file - can be used to demo the FTP (requires DNode1 FTPserver to be running)
	client1.txt 	(This is a test file used for FTP)