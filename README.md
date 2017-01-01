# My little python crawler project
##Scans all subdirectories from a given directory(current directory, or directory from the -d argument)

###Program arguments:

-d Directory that will be crawled(default: current dir)

-f plain text for pattern which will be searched(all files and directories names that will be found must match the pattern(ie. if "el" is given, files like "hello.c" will match)). Escape non alphanum charracters like "./'," and others, to avoid unexpected behaviour.

-re for regex pattern(very similiar to -f)

-a list of file/directory name patterns to be left from the search

-s displays file sizes

If no arguments are used, crawler only writes how many directories and files it came across and exits. More statistics, like number of certain filetypes were present, median, modus of filetypes may be added in future.