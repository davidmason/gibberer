
import os

def ensure_dir(dirName):
    if not os.path.isdir(dirName):
        os.makedirs(dirName)
        
