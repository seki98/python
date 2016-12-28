import os, os.path, sys, re
import argparse

from stat import *

def eexit(message):
    sys.exit("***\n{0}\n***".format(message))

class Scanner:

    def __init__(self, path, filePattern, avoid, mode):
        
        self.dirs = []#all directories that were crawled
        self.files = []#all files that were crawled
        self.searchedFiles = []#files that matched the @filePattern
        self.path = path#path to the first directory to be searched
        self.filePattern = filePattern#filePattern(either regex or plain text)
        self.avoid = avoid#filenames and directory names to be avoided
        self.mode = mode#mode (regex or plain text in the pattern)
        self.maxDepth = 0#max depth found by the Scanner
        self.currDepth = 0#current depth of the scanner
        self.crawl(self.path)#begin the crawling
        
    #crawl selected directory
    def crawl(self, directory):
        if(not os.path.exists(directory)):
            eexit("Directory {0} does not exist".format(directory))
        try:
            os.chdir(directory)
            self.currDepth = self.currDepth + 1
            if(self.currDepth > self.maxDepth):
                self.maxDepth = self.currDepth
        except:
            print("Access denied")
            return
        
        for i in os.listdir("."):
                
            if(self.matches(self.avoid, i, self.mode)):
                    continue
            
                    
            if(S_ISDIR(os.stat(i).st_mode)):
                newDir = Directory(i,os.getcwd())
                self.dirs.append(newDir)
                
                self.crawl(os.getcwd() + "/" +i)
            else:
                newFile = File(i, os.getcwd(),os.stat(i).st_size)
                self.files.append(newFile)        
                if(self.mode != 0):        
                    if(self.matches(self.filePattern, i, self.mode)):
                        self.searchedFiles.append(newFile)

            #print("{0:15} {1:10} {2:10}".format(i,os.stat(i).st_size,fileType))
        os.chdir("..")
        self.currDepth = self.currDepth - 1

    def matches(self, pattern, word, mode):
        #should not look for anything at all
        if(pattern == None or word == None):
            return False

        #pattern is a list, needs to be iterated throufh
        if(isinstance(pattern, list)):
            for i in pattern:
                #plain text is used for re.search
                if( re.search("^.*" + i + ".*$", word, re.IGNORECASE) and self.mode == 1  ):    
                    return True
                #regex is used for re.search
                elif( re.search(pattern, word, re.IGNORECASE) and self.mode == 2):
                    return True
        #plain text is used for re.search
        elif( re.search("^.*" + pattern + ".*$", word, re.IGNORECASE) and self.mode == 1 ):
            return True
        #regex is used for re.search
        elif( re.search(pattern, word, re.IGNORECASE) and self.mode == 2):
            return True
        #no match found
        return False

    def statistics(self):
        for i in self.dirs:
            pass        # print(i.path)
        if(self.searchedFiles):
            print("{0} files matches".format(len(self.searchedFiles)))
            print("{0:15} {1}".format("Filesize", "Filepath"))
            for i in self.searchedFiles:
                print("{0:15}b {1}".format(i.size, i.path +i.name))
            print("This search went through {0} dirs {1} files and got {2} directories deep".format(len(self.dirs), len(self.files), self.maxDepth))

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
    parser.add_argument('-re', action="store", dest="rePattern", help="Regular expression pattern used to search for files", default=None)
    parser.add_argument('-a', action="store", dest="filesToAvoid", help="Filename, dirname or a chain of letters to be avoided", nargs="*", default=[])
    parser.add_argument('-c', action="store", dest="c", type=int)
    args = parser.parse_args()
    if(args.fileToSearch and args.rePattern):
        eexit("You cannot use -re and -f together")
    mode = 0#plain text
    pattern = None
    if(args.fileToSearch):
        pattern = args.fileToSearch
        mode = 1
    if(args.rePattern):
        pattern = args.rePattern
        mode = 2#regex used

    scanner = Scanner(args.dirToCrawl, pattern, args.filesToAvoid, mode)
    scanner.statistics()


if __name__ == "__main__":
    main();
    
    
    