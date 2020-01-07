# for making authorized requests to server
from oauth2client import tools, client, file
# to work with objects
import pickle
# os module
import os


# get and write token to storage.json file
def get_or_write_tokenfile(filename, mode, serverToken=None):
    with open(filename, mode) as tokenfile:
        token = pickle.load(tokenfile) if mode == 'rb' else pickle.dump(serverToken, tokenfile)
    return token


# get the new token from google oauth2
def requestTokenFromGoogle(tokenfilename, credentailsfilename, SCOPES):
    oauth2flow = client.flow_from_clientsecrets(credentailsfilename,
                                                scope=SCOPES)
    token = tools.run_flow(oauth2flow, file.Storage(tokenfilename))
    return token


# get the files from files directory
def getFiles(directorypath):
    return os.listdir(directorypath)


# check the drive
def checkDrive(service, file):
    response = service.files().list(q=f"name='{file}'").execute()
    if len(response.get('files')) > 0:
        for file in response.get('files', []):
            return file.get('id')
    else:
        return 0


# upload new version of files
def uploadNewFileVersion(service, metadata, file):
    resp = service.files().create(body=metadata, media_body=file).execute()
    if resp:
        print(f'Uploaded {resp["name"]} successfully')
    else:
        print(f'Error in uploading {resp["name"]}')
