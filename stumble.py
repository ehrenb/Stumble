"""Stumble.

Usage:
  stumble.py APK_PATHS ...  -s <SEARCH_STRING> ... [-f FILE_TYPES ...] [options]
  stumble.py (-h | --help)
  stumble.py --version

Arguments:
  APK_PATHS the path of the APK you want to search through
  SEARCH_STRING the string(s) you want to search for in a space seperated format

Options:INPUT
  APK_PATHS              The APK path(s) you want to search
  -s SEARCH_STRING  The search string(s) you want to look for
  -f FILE_TYPES           The types of file extensions you want to search (.xml, .txt, etc...)
  --of=<out_format>  The format of the output (JSON,XML,etc)
  -i                              Make search string case insensitive
"""

import os 
from pprint import pprint
import sys

from docopt import docopt

from ApkFileSearch import ApkFileSearch

if __name__ == '__main__':
    arguments = docopt(__doc__, version='0.0.1rc')
    print(arguments)

    apk_paths = arguments['APK_PATHS']
    search_strings = arguments['-s']
    file_types = arguments['-f']

    file_types = [file_type.replace('.','') for file_type in file_types]#remove . from extensions

    print file_types
    #file_types = arguments[]
    #save_files #save files that contain a match
    #out_file #optionally, save results to JSON
    #

    for path in apk_paths:
        if not os.path.isfile(path):
            print '{path} is not a valid file'.format(path=path)
            sys.exit()

    for apk_path in apk_paths:
        afs = ApkFileSearch(apk_path, search_strings, file_types)
        pprint(afs.search())
