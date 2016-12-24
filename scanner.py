import os, os.path, sys
import argparse

from stat import *

def eexit(message):
    sys.exit("***\n{0}\n***".format(message))

class Scanner:

    def __init__(self, path):
        
        self.dirs = []
        self.files = []
        self.path = path
        self.crawl()
        
    
    def crawl(self):
        if(not os.path.exists(self.path)):
            eexit("Directory does not exist")
        os.chdir(self.path)

        print("Scanner initialized")
        print("Current woring directory:\t{0}\n".format(os.getcwd()))
        print("Files present in this directory:")
        print("{0:15} {1:10} {2:10}".format("filename","filesize","filetype"))

        for i in os.listdir("."):
            
            if(S_ISDIR(os.stat(i).st_mode)):
                newDir = Directory(i,os.getcwd())
                self.dirs.append(newDir)
            else:
                newFile = File(i, os.getcwd(),os.stat(i).st_size)

            #print("{0:15} {1:10} {2:10}".format(i,os.stat(i).st_size,fileType))

    def statistics(self):
        for i in self.dirs:
            pass        # print(i.path)

class Directory:
    def __init__(self,name,path):
        self.name = name
        self.path = path + "/" + name

class File:
    def __init__(self, name, path, size):
        self.path = path
        self.size = size        
        self.name, self.ext = os.path.splitext(path + name)
        # print(self.ext)

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan directory tree of the chosen or current directory")
    
    parser.add_argument('-d', action="store", dest="dirToCrawl", help="Path to the target directory(default: current dir)", default=os.getcwd())
    parser.add_argument('-f', action="store", dest="fileToSearch", help="Write filename or a chain of letters which will find exact or similiar files")
    parser.add_argument('-c', action="store", dest="c", type=int)
    args = parser.parse_args()

    
    scanner = Scanner(args.dirToCrawl);
    scanner.statistics();
    
    