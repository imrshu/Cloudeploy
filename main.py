# calling the google api's
from googleapiclient import discovery
# for setting up Http connection
from httplib2 import Http
# import helper functions
from helpers import (get_or_write_tokenfile,
                    requestTokenFromGoogle,
                    getFiles, checkDrive,
                    uploadNewFileVersion,
                    checkFolder,
                    createFolder,
                    uploadFilesToDir)
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
        print(f'Older {file} deleted successfully')
        return True
    else:
        return False


# Delete the folder from drive
def deleteFolder(service, folderId):
    service.files().delete(fileId=folderId).execute()


# upload file to drive
def uploadFile(tokenfilename, credentailsfilename, directorypath, parentID=None):
    start_time = time.time()
    service = getToken(tokenfilename, credentailsfilename)
    for file in getFiles(directorypath):
        # Get the sub directory absolute path
        subdir_filepath = os.path.join(directorypath, file)
        if os.path.isdir(subdir_filepath):
            # Create metadata for folder
            dir_metadata = {'name': file, 'mimeType': 'application/vnd.google-apps.folder', 'parents': ['1pmFLZ-sNeLscJ9pmqA2CPmcYv8FyF2iv']}
            # Check if folder exists
            oldFolderId = checkFolder(service, file)
            if oldFolderId != 0:
                # Delete the old folder of files
                deleteFolder(service, oldFolderId)
            # Create the new folder
            newFolderId = createFolder(service, dir_metadata)
            # Upload files to folder
            uploadFilesToDir(service, subdir_filepath, newFolderId)
            print(f'Process completed in {time.time() - start_time} seconds...')
        else:
            # Create file metadata
            file_metadata = {'name': file, 'mimeType': file.split('.')[1], 'parents': ['1pmFLZ-sNeLscJ9pmqA2CPmcYv8FyF2iv']}
            # If file exists delete the file
            if deleteFile(service, file):
                # Upload new version of file
                uploadNewFileVersion(service, file_metadata, os.path.join(directorypath, file))
            else:
                # Upload new version of file
                uploadNewFileVersion(service, file_metadata, os.path.join(directorypath, file))
            print(f'Process completed in {time.time() - start_time} seconds...')


if __name__ == '__main__':
    # For command line arguments
    uploadFile('storage.json', 'credentials.json', './files')
