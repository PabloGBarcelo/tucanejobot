import requests
import base64
import os

def uploadFile(rootdir, fileName, url, apikey):
    # open binary file
    print(rootdir + "\\" + fileName)
    with open(rootdir + "\\" + fileName, "rb") as f:
        file = base64.b64encode(f.read())
    # upload to server via FTP?
    dataHost = requests.post(url,{
        "key": apikey,
        "image": file,
        "name": fileName
    })
    os.remove(fileName)
    # return url
    return dataHost.json()