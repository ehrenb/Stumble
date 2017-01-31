from pprint import pprint
import re

from androguard.core.bytecodes.apk import APK
import magic

class ApkFileSearch(object):
    def __init__(self, apk_file, search_strings, file_types, case_sensitive=True):
        self.apk = APK(apk_file)
        self.search_strings = search_strings
        self.file_types = file_types

        flags = 0
        if not case_sensitive:
            flags = re.IGNORECASE
        self.patterns = [re.compile(search_string, flags=flags) for search_string in search_strings]

    def search(self):
        apk_files = self.apk.get_files_types()
        search_results = []
        for file_path, file_type in apk_files.iteritems():
            if any(interested_type in file_type.lower() for interested_type in self.file_types):
                file_data = self.apk.get_file(file_path)

                for pattern in self.patterns:
                        match = pattern.search(file_data)
                        if match:
                            search_result = {'file_path': file_path,
                                                      'file_type': file_type,
                                                      'search_string': pattern.pattern,
                                                      'match': match.group(0)}
                            search_results.append(search_result)
        return search_results
