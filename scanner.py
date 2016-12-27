import os, os.path, sys, re
import argparse

from stat import *

def eexit(message):
    sys.exit("***\n{0}\n***".format(message))

class Scanner:

    def __init__(self, path, filePattern, avoid):
        
        self.dirs = []
        self.files = []
        self.path = path
        self.filePattern = filePattern
        self.avoid = avoid
        self.crawl(self.path)
        
    #crawl selected directory
    def crawl(self, directory):
        if(not os.path.exists(directory)):
            eexit("Directory {0} does not exist".format(directory))
        os.chdir(directory)

        
        for i in os.listdir("."):
                
            if(self.matches(self.avoid, i)):
                    continue
            
                    
            if(S_ISDIR(os.stat(i).st_mode)):
                newDir = Directory(i,os.getcwd())
                self.dirs.append(newDir)
                
                self.crawl(os.getcwd() + "/" +i)
            else:
                    
                
                if(self.matches(self.filePattern, i)):
                    newFile = File(i, os.getcwd(),os.stat(i).st_size)
                    self.files.append(newFile)

            #print("{0:15} {1:10} {2:10}".format(i,os.stat(i).st_size,fileType))
        os.chdir("..")

    def matches(self, pattern, word):
        if(pattern == None or word == None):
            return False
        if(isinstance(pattern, list)):
            for i in pattern:
                if( re.search("^.*" + i + ".*$", word, re.IGNORECASE)  ):    
                    return True
        elif( re.search("^.*" + pattern + ".*$", word, re.IGNORECASE)  ):
            return True
        return False

    def statistics(self):
        for i in self.dirs:
            pass        # print(i.path)
        if(self.files):
            print("Files matches")
            print("{0:15} {1}".format("Filesize", "Filepath"))
            for i in self.files:
                print("{0:15}b {1}".format(i.size, i.path +i.name))
        # if(self.dirs):
        #     print("Dirs matches")
        #     print(*self.dirs, sep="\n")
class Directory:
    def __init__(self,name,path):
        self.name = name
        self.path = path + "/" + name

class File:
    def __init__(self, name, path, size):
        self.path = path + "/"
        self.size = size        
        self.name = name
        
        # print(self.ext)

    
def main():
    parser = argparse.ArgumentParser(description="Scan directory tree of the chosen or current directory")
    
    parser.add_argument('-d', action="store", dest="dirToCrawl", help="Path to the target directory(default: current dir)", default=os.getcwd())
    parser.add_argument('-f', action="store", dest="fileToSearch", help="Filename, dirname or a chain of letters which will find exact or similiar files", default=None)
    parser.add_argument('-a', action="store", dest="filesToAvoid", help="Filename, dirname or a chain of letters to be avoided", nargs="*", default=[])
    parser.add_argument('-c', action="store", dest="c", type=int)
    args = parser.parse_args()

    
    scanner = Scanner(args.dirToCrawl, args.fileToSearch, args.filesToAvoid)
    scanner.statistics()


if __name__ == "__main__":
    main();
    
    
    