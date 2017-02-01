"""Stumble.

Usage:
  stumble.py APK_PATHS ...  -s <SEARCH_STRING> ... [-f FILE_TYPES ...] [options]
  stumble.py APK_PATHS ... -f FILE_TYPES ... [-w OUT_DIR] [-o FILE_NAME]
  stumble.py (-h | --help)
  stumble.py --version

Arguments:
  APK_PATHS the path of the APK you want to search through
  SEARCH_STRING the string(s) you want to search for in a space seperated format

Options:
  APK_PATHS              The APK path(s) you want to search
  -s SEARCH_STRING  The search string(s) you want to look for
  -f FILE_TYPES           The types of file extensions you want to search (.xml, .txt, etc...)
  -i --insensitive          Make search string case insensitive
  -o FILE_NAME           Write a result summary JSON file to FILE_NAME
  -w OUT_DIR              Save matched files to OUT_DIR directory
"""

import json
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
    is_case_insensitive = arguments['--insensitive']
    output_file_name = arguments['-o']
    save_matched_files_dir = arguments['-w']

    file_types = [file_type.replace('.','') for file_type in file_types]#remove . from extensions

    print file_types
    #file_types = arguments[]
    #save_files #save files that contain a match
    #out_file #optionally, save summary results to JSON
    #

    for path in apk_paths:
        if not os.path.isfile(path):
            print '{path} is not a valid file'.format(path=path)
            sys.exit()

    #initialize a file with an empty JSON array
    if output_file_name:
        with open(output_file_name, 'a') as f:
            json.dump([], f)

    for apk_path in apk_paths:
        afs = ApkFileSearch(apk_path, 
                                        search_strings,
                                        file_types,
                                        case_insensitive=is_case_insensitive,
                                        save_matched_files_dir=save_matched_files_dir)
        results = afs.search()
        pprint(results)
        #load existing JSON data, append, and re-dump it
        if output_file_name and os.path.exists(output_file_name):
            with open(output_file_name,'r') as f:
                data = json.load(f)
            #key as apk name for identifier
            results = {apk_path:results}
            data.append(results)
            with open(output_file_name,'w') as f:
                json.dump(data, f, sort_keys=True,
                                             indent=4,
                                             separators=(',',': '))
