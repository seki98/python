import os, os.path, sys, re, logging
import argparse

from stat import *



def elog(message):
    logging.exception(message)
    logging.info("\n")

def eexit(message):
    sys.exit("***\n{0}\n***".format(message))

class Scanner:

    def __init__(self, settings, filePattern, avoid):
        
        self.dirs = []#all directories that were crawled
        self.files = []#all files that were crawled
        self.searchedFiles = []#files that matched the @filePattern
        self.searchedDirs = []#dirs that matched the @filePattern

        self.path = settings.path#path to the first directory to be searched
        self.filePattern = filePattern#filePattern(either regex or plain text)
        self.avoid = avoid#filenames and directory names to be avoided
        
        self.mode = settings.mode#mode (regex or plain text in the pattern)
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
            #os.chdir failed
            elog("changedir denied in {}".format(directory))
            return
        
        try:
            for i in os.listdir("."):
                    
                if(self.matches(self.avoid, i, self.mode)):
                    continue    
                                
                        
                if(S_ISDIR(os.stat(i).st_mode)):
                    newDir = Directory(os.getcwd() +'/'+i )
                    self.dirs.append(newDir)
                    
                    self.crawl(os.getcwd() + "/" +i)
                    os.chdir("..")
                    self.currDepth = self.currDepth - 1
                    if(self.matches(self.filePattern, i, self.mode)):
                            self.searchedDirs.append(newDir)
                else:
                    newFile = File(i, os.getcwd(),os.stat(i).st_size)
                    self.files.append(newFile)        
                    if(self.mode != 0):        
                        if(self.matches(self.filePattern, i, self.mode)):
                            self.searchedFiles.append(newFile)

                #print("{0:15} {1:10} {2:10}".format(i,os.stat(i).st_size,fileType))
        except:
            #os.listdir failed
            elog("listdir denied in {}".format(os.getcwd()))
            return

    #pattern-either pattern for avoiding files, or for finding files(based on "mode")
    #word-checking pattern matches in "word"
    #mode-checking mode for pattern type| mode1 = plain, mode2 = regex
    def matches(self, pattern, word, mode):
        #should not look for anything at all
        if(pattern == None or word == None):
            return False
        #pattern is a list, needs to be iterated through
        if(isinstance(pattern, list)):
            for i in pattern:
                #plain text is used for re.search
                if( re.search("^.*" + i + ".*$", word, re.IGNORECASE) and self.mode == 1  ):    
                    return True
                #regex is used for re.search
                elif( re.search(i, word, re.IGNORECASE) and self.mode == 2):
                    return True
        #plain text is used for re.search
        elif( re.search("^.*" + pattern + ".*$", word, re.IGNORECASE) and self.mode == 1 ):
            return True
        #regex is used for re.search
        elif( re.search(pattern, word, re.IGNORECASE) and self.mode == 2):
            return True
        #no match found
        return False

    def statistics(self, settings):
        
        if(self.searchedFiles or self.searchedDirs):
            #display all the searched dirs and files 
            print("{} files matches\n---------------------".format(len(self.searchedFiles)))
            print("{:15} {}".format("Filesize", "Filepath"))
            for i in self.searchedDirs:
                print("Directory: {}".format(i.path))
            for i in self.searchedFiles:
                if(settings.displaySize):
                    print("{:15}b {}".format(i.size, i.path +i.name))
                else:
                    print(i.path + i.name)
            print("---------------------\nFile matches are above")
        else:
            #no files or dirs matched the criteria
            if(settings.search == 1):
                print("No files matched the criteria\n")
        print("This search went through {} dirs {} files and got {} directories deep".format(len(self.dirs), len(self.files), self.maxDepth))

class Directory:
    def __init__(self,path):
        self.path = path + "/"

class File:
    def __init__(self, name, path, size):
        self.path = path + "/" + name
        self.size = size        
        self.name = name
        
        # print(self.ext)
class Settings:
    def __init__(self):
        pass
    
def main():
    parser = argparse.ArgumentParser(description="Scan directory tree of the chosen or current directory")
    
    #d - directory that will be crawled
    #f - plain text that will be looked for anywhere in the directory/file names
    #re - regex that will be search for in directory/file names
    #a - search will ignore any file or directory that matches any of the list members of a
    #s - search will show searched files with their file sizes
    parser.add_argument('-d', action="store", dest="dirToCrawl", help="Path to the target directory(default: current dir)", default=os.getcwd())
    parser.add_argument('-f', action="store", dest="fileToSearch", help="Filename, dirname or a chain of letters which will find exact or similiar file names. CAUTION: When using non-alphanumerical characters, put '\\' before each of them, otherwise unexpected behaviour might occur", default=None)
    parser.add_argument('-re', action="store", dest="rePattern", help="Regular expression pattern used to search for files", default=None)
    parser.add_argument('-a', action="store", dest="filesToAvoid", help="Filename, dirname or a chain of letters to be avoided", nargs="*", default=[])
    parser.add_argument('-s', action="store_true", dest="displaySize", help="Display sizes of files found", default=False)
    
    #process the arguments
    args = parser.parse_args()
    
    #Do not allow using regex and plain text as pattern at the same time
    if(args.fileToSearch and args.rePattern):
        eexit("You cannot use -re and -f together")
    
    #plain text or regex that will be searched
    pattern = None

    #set settings for scanning
    settings = Settings()
    settings.mode = 0#no pattern used so far
    settings.search = 0#do not search for anything
    if(args.fileToSearch):
        pattern = args.fileToSearch
        settings.mode = 1#plain text used
        settings.search = 1
    if(args.rePattern):
        pattern = args.rePattern
        settings.mode = 2#regex used
        settings.search = 1

    #save info whether file sizes should be displayed
    settings.displaySize = False if not args.displaySize else True
    settings.path = args.dirToCrawl

    #delete log file if it exists already for clean log
    try:
        os.remove("error.log")
    except OSError:
        pass

    #set log file
    logging.basicConfig(level=logging.DEBUG, filename='error.log')

    #create Scanner and scan
    scanner = Scanner(settings, pattern, args.filesToAvoid)

    #show scan results
    scanner.statistics(settings)


if __name__ == "__main__":
    main();
    
    
    