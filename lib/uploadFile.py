import requests
import base64
import os
from definitions import SLASH
def uploadFile(rootdir, fileName, url, apikey):
    # open binary file
    with open(rootdir + SLASH + fileName, "rb") as f:
        file = base64.b64encode(f.read())
    # upload to server via FTP?
    dataHost = requests.post(url,{
        "key": apikey,
        "image": file,
        "name": fileName
    })
    os.remove(fileName)
    os.remove(fileName.replace("jpg", "png"))
    # return url
    return dataHost.json()