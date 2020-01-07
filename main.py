# calling the google api's
from googleapiclient import discovery
# for setting up Http connection
from httplib2 import Http
# import helper functions
from helpers import (get_or_write_tokenfile,
                    requestTokenFromGoogle,
                    getFiles, checkDrive,
                    uploadNewFileVersion)
# os module to work with directories & files
import os
# time library for measuring time
import time


# Define the permissions to be asked from user for granting to application
# for further scopes visit link- https://developers.google.com/drive/api/v3/about-auth
SCOPES = 'https://www.googleapis.com/auth/drive'


# Retrieve token
def getToken(tokenfilename, credentailsfilename):
    if os.path.exists(tokenfilename):
        token = get_or_write_tokenfile(tokenfilename, 'rb')
        if not token or token.invalid:
            token = requestTokenFromGoogle(tokenfilename, credentailsfilename)
            get_or_write_tokenfile(tokenfilename, 'wb', token)
    else:
        token = requestTokenFromGoogle(tokenfilename, credentailsfilename, SCOPES)
        get_or_write_tokenfile(tokenfilename, 'wb', token)

    return discovery.build('drive', 'v3', http=token.authorize(Http()))


# update the file in drive
def deleteFile(service, file):
    id = checkDrive(service, file)
    if id:
        service.files().delete(fileId=id).execute()
        print(f'Older version of {file} deleted successfully')
        return True
    else:
        return False


# upload file to drive
def uploadFile(tokenfilename, credentailsfilename, directorypath, parentID=None):
    service = getToken(tokenfilename, credentailsfilename)
    start_time = time.time()
    for file in getFiles(directorypath):
        metadata = {'name': file, 'mimeType': file.split('.')[1], 'parents': [parentID]}
        if deleteFile(service, file):
            uploadNewFileVersion(service, metadata, directorypath+file)
            print(f'Process completed in {time.time() - start_time} seconds...')
        else:
            uploadNewFileVersion(service, metadata, directorypath+file)
            print(f'File uploaded in {time.time() - start_time} seconds...')


if __name__ == '__main__':
    # For command line arguments
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--parent', help='Enter the drive folder ID')
    parser.add_argument('-c', '--credentials', help='Give path to credentials.json file')
    parser.add_argument('-f', '--file', help='Give path to files directory')
    args = parser.parse_args()
    if args.parent and (args.credentials and args.file):
        uploadFile('storage.json', args.credentials, args.file, args.parent)
    else:
        print('Values were not given Try again....')
