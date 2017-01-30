from pprint import pprint

from androguard.core.bytecodes.apk import APK
import magic

a = APK('banking_malware.apk')
#get_files_types

apk_files = a.get_files_types()


interested_types = ['ascii','xml']
interested_phrases = ['http://']

for file_path, file_type in apk_files.iteritems():
    print file_type
    if any(interested_type in file_type.lower() for interested_type in interested_types):
        file_data = a.get_file(file_path)

        if any(interested_phrase in file_data for interested_phrase in interested_phrases):
            print file_path
            print True
            break
