# -*- coding: utf-8 -*-
"""
=================== CLIENT ===================

"""
import os, rpyc
import pandas as pd
import ftplib
    
cpath = r"C:\Temp\TMP\DFS\Client"  # Specify the client directory
#os.chdir(cpath)     # Change the active directory of the client- location where files can be uploaded from and downloaded in the client

# Function to connect to the FTP server for a DNode & then perform file actions
def connect(host,port,flag, file):
    print ("Host: {}, Port:{}, Opt Code: {}, filename: {}".format(host, port, flag, file))
                                     # Takes 4 arguments: Host IP, Host FTP Port, flag containg file action, filename 
    try:
        ftp = ftplib.FTP('')
        ftp.connect(host,int(port))  # FTP connects to the host: port  {int value of port}
        while True:
            username = input("Please enter FTP username: ")   # Requests the user for FTP username
            passwd = input("Please enter password for {} : ".format(username))   # Requests the password for entered username
            try:
                ftp.login(str(username),str(passwd))
                print ("Conencted to FTP Server {}:{}".format(host,port)) # Tries to login FTP server using given credentials
                print ("Files in cwd:\n")   
                ftp.dir()                           # Upon connecting, lists the contents of the root directory of the user
                if flag==2:
                    retcode = upload(ftp, file)     # Option 2 is for uploading a file from client to connected DNode
                elif flag==3:                       # Option 3 is for downloading a file from connected DNode to client
                    localfiles = getlocalfiles()     
                    print ("Current list of local files in client:\n{}\nTotal file count = {}".format(localfiles, len(localfiles)))
                                                    # Prints the contents & total files in the client directory BEFORE download
                    retcode = download(ftp, file)   # Calls the function that downloads the file using ftp connection & Filename as args
                    newlocalfiles = getlocalfiles()
                    print ("Updated list of local files in client:\n{}\nTotal file count = {}".format(newlocalfiles, len(newlocalfiles)))
                                                    # Prints the contents & total files in the client directory AFTER download
                elif flag==4:                       # Option 4 is for deleting a file from connected DNode
                    retcode = deletefile(ftp, file) # Calls the function that deletes the given file from it's DNode
                return (retcode)                    # Returns the return code from the called function    
            except:
                print ("Incorrect Username or Password. Please try again...")  # Prints login error when incorrect credentials are entered
    except ftplib.all_errors as error:              # Check for any ftplib error & print/ return it back
        print (error)
        return (error)

# Function to upload a given file to the connected DNode
def upload(ftp, ufile):
    try:
        print ("Starting upload....")
        ftp.storbinary("STOR "+ ufile , open (ufile, 'rb')) # start uploading the file to DNode FTPserver (opens the file as read-binary in the client)
        print ("File ", ufile, "uploaded successfully from client to DNode...\n")
        print ("Updated files in cwd:")
        ftp.dir()                                   # Prints the updated files in the FTP server directory after upload
        print ("Disconnecting from server")
        ftp.quit()                                                       # Close the FTP connection
        return ('250-Requested file action completed')
    except ftplib.all_errors as error:              # Check for any ftplib error & print/ return it back
        print (error)
        return ("426-Connection closed; File action aborted")

# Function to download a given file to the Client from the connected DNode
def download(ftp, dfile):
    try:
        print ("Starting download....")
        ftp.retrbinary("RETR " + dfile, open (dfile, 'wb').write, 1024)  # start downloading the file from DNode FTPserver 
                                                                         # opens the file as write-binary in the client, writing 1024 blocks at a time (buffer)
        print ("File ", dfile, "Downloaded successfully from DNode to client...")
        print ("Disconnecting from server")
        ftp.quit()                                                       # Close the FTP connection
        return ('250-Requested file action completed')
    except ftplib.all_errors as error:              # Check for any ftplib error & print/ return it back
        print (error)
        return ("426-Connection closed; File action aborted")

# Function to delete a given file from it's DNode
def deletefile(ftp, xfile):
    try:
        print ("Deleting file...")
        ftp.delete(xfile)                           # Deletes the given file from it's DNode
        print ("File ", xfile, "deleted successfully...")
        print ("Updated files in cwd:")             # Prints the updated files in the FTP server directory after deletion
        ftp.dir()
        print ("Disconnecting from server")
        ftp.quit()                                                       # Close the FTP connection
        return ('250-Requested file action completed') 
    except ftplib.all_errors as error:              # Check for any ftplib error & print/ return it back
        print (error)
        return ("426-Connection closed; File action aborted")
    
    
# Function to get the list of files from the local client directory
def getlocalfiles():
    flist = []                                           # Create a blank list               
    for (dirpath, dirnames, filename) in os.walk(cpath): # Iterate through the folder, file in the given client path
        for file in filename:
            flist.append(file)                           # append each file to the list                              
    return (flist)                                       # Return the updated file list                   

# Function to get the details of a randomly selected DNode for file upload 
def get_DNode_info(master):
    dnode = master.select_dn()              # Calls the exposed function in the Master server 
    print ("""Selected Data Node:
        Node_IP:{}
        Node_Port:{}
        Node_Directory: {}\n""".format(dnode[0],dnode[1],dnode[2]))
    return (dnode[0],dnode[1],dnode[2])     # Return the details of the selected DNode

def main():
    host = input("Enter the server IP [Default = 127.0.0.1]:") # Requests the user to input the IP of the Master server to be connected
    if host:
        pass                                                   # In case of user input, do nothing 
    else:
        host = "127.0.0.1"                                     # IN case of NO User input, set default Master server IP         
    port = input("Enter the server port [Default = 18812]:")   # Requests the user to input the Port number of the Master server to be connected
    if port:
         pass                                                  # In case of user input, do nothing
    else:
        port = 18812                                           # IN case of NO User input, set default Master server port
    con=rpyc.connect(host,port)                                # Connect to the Master server IP: Port
    print ("Connected to MasterServer [{}]:{}".format(host,port))
    master=con.root.Master()                                   # Allows calling of exposed remote Master server functions
                                    # Instructions for Reuse
    instructions = """Please select an option [0-4]:
    1. Get file list
    2. Upload a file
    3. Download a file
    4. Delete a file
    0. Quit\n
Input Opton >>> """
    while master:
        try:
            opt = input(instructions)                          # Request user for an input based on printed instructions
            opt = int(opt)                                     # Convert the user input to int
            if opt in range(5):                                # Check if the user input is in range [0-4] 
                if opt== 0:
                    break                             # Option 0 Quits the program 
                elif opt ==1:                         # Option 1 is for listing all the files across all connected DNodes 
                    flist = master.filemap()                   # Get the file list across all DNodes from the Master server function
                    with pd.option_context('max_colwidth', 1000, 'display.max_columns', 500):
                        print (flist,"\n\n\n")                 # Print the dataframe with all file info 
                elif opt ==2:                         # Option 2 is for uploading a file from client to connected DNode       
                    print ("Fetching upload server details...")
                    DN_HOST,DN_PORT,DN_PATH = get_DNode_info(master) # Get a random DNode server to upload the file
                    ftpport = DN_PORT + 1                            # FTP port for each DNode is the following port of the DNode rpyc server
                    localfiles = getlocalfiles()                     # Prints the contents & total files in the client directory for user to select
                    print (localfiles)
                    ufile = input("Please enter the filename to upload to DNode: ") # Request user to enter the filename to be uploaded
                    if ufile in localfiles:                                         # Check if the user input filename exists in the local directory
                        try:
                            print ("Connecting to ftpserver...")
                            msgcode = connect(DN_HOST, ftpport, opt, str(ufile))    # If file exists, share the required args to Connect() function
                            print (msgcode, "\n\n")                                 # Print the returned code from the Connect() function    
                        except ftplib.error_perm as error:
                            print (error)                                           # Print any file permission errors encountered during upload
                    else:
                        print ("No such file found at ", cpath, "\n\n\n")           # Print error message if no file found
                elif opt ==3:
                    key = input("Enter the keyword to search the required file for download [Default = List all files] : ")
                                                                        # Reuqest user for a keyword search - this matches the keyword to all files across all DNodes
                    if key:
                        try:
                            match = master.Matchfile(key)               # Match the user input with the filenames using Master server function
                            mdf = pd.DataFrame(match)
                            print(mdf)
                        except:
                            print ("No matching files found\n\n\n")     # Print error if no file match found
                    else:
                        match = master.filemap()                        # In case of no user input, display all files across all DNodes
                        print (match,"\n")
                    dfile = input("Please enter the filename to be downloaded to client: ") # Request user input for name of file to be uploaded
                    mdict = master.Matchfile(dfile)                     # Get the matched dictionary from Master Server 
#                    print (mdict)
#                    print (type(mdict))
                    mf = pd.DataFrame(mdict)                            # Convert the dictionary to a pandas dataFrame
#                    print (type(mf))
                    print (mf)
                    host, port = mf.at[0,'DN_IP'], mf.at[0,'DN_Port'] + 1 # Get the details of DNode that contains the file
                    print ("Connecting to ftpserver...")
                    msgcode = connect(host, port, opt, str(dfile))      # Connect to the DNode with required args
                    print (msgcode, "\n\n")
                elif opt == 4:                        # Option 4 is for deleting a file from connected DNode
                    flist = master.filemap()
                    print ("List of available files: ", flist, "\n")    # Print the currently available files
                    xfile = input("Name of the file to be deleted: ")
                    try:
                        xdict = master.Matchfile(xfile)                 # Get the matched dictionary from Master Server 
#                        print (xdict)
#                        print (type(xdict))
                        xf = pd.DataFrame(xdict)                        # Convert the dictionary to a pandas dataFrame
                        print (xf)
                        host, port = xf.at[0,'DN_IP'], xf.at[0,'DN_Port'] + 1 # Get the details of DNode that contains the file
                        print ("Connecting to ftpserver...")
                        msgcode=connect(host, port, opt, str(xfile))    # Connect to the DNode with required args
                        print (msgcode, "\n\n")
                        print ("Disconnecting from server\n")
                    except:
                        print ("Unidentified Error")
                else:
                    break
        except:
            print ("Unidentified input")                # Print error if user input is out of range or not a digit
    print ("Quitting Program\nThank you!")              # Print if Opt=0 & quit

if __name__ == "__main__":
    main()                                              # Call & execute main program