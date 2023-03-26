from definitions import SLASH

def getDirectory(folders):
    path = ""
    for folder in folders:
        path+= SLASH + folder
    
    return path + SLASH