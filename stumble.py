"""Stumble.

Usage:
  stumble.py APK_PATHS ...  -s <SEARCH_STRING> ... [options]
  stumble.py (-h | --help)
  stumble.py --version

Arguments:
  APK_PATHS the path of the APK you want to search through
  SEARCH_STRING the string(s) you want to search for in a space seperated format

Options:INPUT
  APK_PATHS          The APK path(s) you want to search
  -s SEARCH_STRING  The search string(s) you want to look for
  --of=<out_format>  The format of the output (JSON,XML,etc)

"""

import os 
import sys

from docopt import docopt


if __name__ == '__main__':
    arguments = docopt(__doc__, version='0.0.1rc')
    print(arguments)

    apk_paths = arguments['APK_PATHS']
    search_strings = arguments['-s']
    #file_types = arguments[]
    #save_files #save files that contain a match
    #out_file #optionally, save results to JSON
    #

    for path in apk_paths:
        if not os.path.isfile(path):
            print '{path} is not a valid file'.format(path=path)
            sys.exit()
