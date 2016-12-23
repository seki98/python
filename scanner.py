import os
from stat import *

print("Current woring directory:\t{0}\n".format(os.getcwd()))
print("Files present in this directory:")
print("{0:15} {1:10} {2:10}".format("filename","filesize","filetype"))
class Scanner:
    def __init__(self):
        print("Scanner initialized")
        
    
    def crawl(self):
        for i in os.listdir("."):
            fileMode = os.stat(i).st_mode
            if(S_ISDIR(fileMode)):
                fileType = "DIR"
            else:
                fileType = "FILE"
            print("{0:15} {1:10} {2:10}".format(i,os.stat(i).st_size,fileType))
    
    
    
if __name__ == "__main__":
    scanner = Scanner();
    
    