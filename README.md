# Cloudeploy
A command line script or tool for upload files to google drive


## Prerequisites
* For windows users, they mush have installed Python on their system.
* For linux users, they must have upgrade to Python 3.x version.
* For mac OSx users, they must have also upgrade to Python 3.x version.

## Steps to run the tool
* Open terminal or Command prompt
* Run this command `pip3 install google-api-python-client`
* Run this command `pip3 install oauth2client`
* Now clone this repository
* Change the directory to cloned folder
* Run the script as `python3 main.py -p <Folder Id> -c <Credentials.json file> -f <Files Directory>`

### Abbreviations
* Folder Id - Give folder id of the folder at your google drive to where you want to store your files in drive.
* Credentials.json file - Give absolute path of your `credentials.json` file which you got by configuring or enabling the drive api at this link- `https://console.developers.google.com/flows/enableapi?apiid=drive`
* Files Directory- Give absolute path of the directory where all your files are stored and you want to upload them to the a specific folder in google drive.
