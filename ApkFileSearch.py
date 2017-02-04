import os
from pprint import pprint
import re

from androguard.core.bytecodes.apk import APK, AXMLPrinter
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
        """iterate through files in the APK and apply search_strings over files that are of type file_types
            if no search strings specified, consider all files a match
            if no file_types specified, apply search strings to all files
            if no search strings and no file types, then return all files
        """
        apk_files = self.apk.get_files_types()
        search_results = []
        for file_path, file_type in apk_files.iteritems():
            file_ext = os.path.splitext(os.path.basename(file_path))[1]

            #if file type filter on, and this file is not that type, then skip
            if self.file_types and not any(interested_type in file_type.lower() or interested_type in file_ext for interested_type in self.file_types):
                continue

            search_result = None
            file_data = self.apk.get_file(file_path)

            if self.search_strings:
                for pattern in self.patterns:
                        match = pattern.search(file_data)
                        if match:
                            search_result = {'file_path': file_path,
                                                      'file_type': file_type,
                                                      'search_string': pattern.pattern}
                            search_results.append(search_result)
            else:
                search_result = {'file_path': file_path,
                                          'file_type': file_type,
                                          'search_string': None}
                search_results.append(search_result)

            #write individual files
            if search_result and self.save_matched_files_dir:
                #save original structure to avoid duplicate filename collisions
                save_file_path = os.path.join(self.save_matched_files_dir, file_path)
                if not os.path.exists(os.path.dirname(save_file_path)):
                    os.makedirs(os.path.dirname(save_file_path))

                with open(save_file_path,'wb') as f:
                    f.write(file_data)

                if 'Android binary XML' in file_type:
                    with open(save_file_path,'r+') as axml_f:
                        decoded_axml = AXMLPrinter(axml_f.read()).buff
                        axml_f.seek(0)
                        axml_f.write(decoded_axml)
                        axml_f.truncate()

        return search_results
