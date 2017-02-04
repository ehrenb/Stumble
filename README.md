# Stumble
Stumble is a small command-line tool for searching and extracting static files packaged inside of APKs.  

```
Usage:
  stumble.py APK_PATHS ...  [-s <SEARCH_STRING>] ... [-f FILE_TYPES ...] [options]

  stumble.py (-h | --help)
  stumble.py --version

Arguments:
  APK_PATHS the path of the APK you want to search through
  SEARCH_STRING the string(s) you want to search for in a space seperated format
  FILE_TYPES The types of file extensions you want to search (.xml, .txt, etc...)
  FILE_NAME Result file to write JSON summary to
  OUT_DIR Save file(s) matched, if no FILE_TYPES specified, then save ALL files

Options:
  -s SEARCH_STRING  The search string(s) you want to look for
  -f FILE_TYPES           Specify the types of file extensions you want to search (.xml, .txt, etc...)
  -i --insensitive          Make search string case insensitive
  -o FILE_NAME           Write a result summary JSON file to FILE_NAME
  -w OUT_DIR              Save matched files to OUT_DIR directory
  ```
  
  
  
# Examples:
Extract all files whose data matches a regular expression 'http://' or 'android' into a directory 'output':

```
python stumble.py banking_malware.apk -s http:// -s android -w output
```

Extract only JSON and XML files whose data matches a regular expression 'http://' into a directory 'output'

```
python stumble.py banking_malware.apk -f json -f xml -s http:// -s android -w output
```

Extract all files to a directory 'output':

```
python stumble.py banking_malware.apk -w output
```
