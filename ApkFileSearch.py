import os
from pprint import pprint
import re

from androguard.core.bytecodes.apk import APK
import magic

class ApkFileSearch(object):
    def __init__(self, 
                      apk_file, 
                      search_strings, 
                      file_types, 
                      case_insensitive=False,
                      save_matched_files_dir=None):
        self.apk = APK(apk_file)
        self.search_strings = search_strings
        self.file_types = file_types

        self.save_matched_files_dir = None
        if save_matched_files_dir:
            self.save_matched_files_dir = os.path.join(save_matched_files_dir, os.path.splitext(os.path.basename(apk_file))[0])
            os.makedirs(self.save_matched_files_dir)

        flags = 0
        if case_insensitive:
            flags = re.IGNORECASE
        self.patterns = [re.compile(search_string, flags=flags) for search_string in search_strings]

    def search(self):
        apk_files = self.apk.get_files_types()
        search_results = []
        for file_path, file_type in apk_files.iteritems():
            file_ext = os.path.splitext(os.path.basename(file_path))[1]
            print file_ext
            #if file_type option on, and this file is not that type, then skip
            if self.file_types and not any(interested_type in file_type.lower() or interested_type in file_ext for interested_type in self.file_types):
                continue

            search_result = None

           #record all files of specified file_type
            if self.file_types and not self.search_strings:
                search_result = {'file_path': file_path,
                                           'file_type': file_type,
                                           'search_string': None}
                search_results.append(search_result)

            file_data = self.apk.get_file(file_path)

            for pattern in self.patterns:
                    match = pattern.search(file_data)
                    if match:
                        search_result = {'file_path': file_path,
                                                 'file_type': file_type,
                                                 'search_string': pattern.pattern}
                        search_results.append(search_result)

            if search_result and self.save_matched_files_dir:
                #save original structure to avoid duplicate filename collisions
                save_file_path = os.path.join(self.save_matched_files_dir, file_path)
                if not os.path.exists(os.path.dirname(save_file_path)):
                    os.makedirs(os.path.dirname(save_file_path))

                with open(save_file_path,'wb') as f:
                    f.write(file_data)

        return search_results
