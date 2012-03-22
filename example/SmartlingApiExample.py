import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path) # allow to import ../apisdk/SmartlingFileApi

from apisdk.SmartlingFileApi import SmartlingFileApi

class FileProperties:
    def __init__(self, path, name, type):
        self.path = path
        self.name = name
        self.type = type

class SmartlingApiExample:
    
    HOST           = 'sandbox-api.smartling.com'
    MY_API_KEY     = "00212573-255a-4ced-87bc-005be5861d45"
    MY_PROJECT_ID  = "f4c6f2413"
    
    def __init__(self, fileProps, locale):
        self.fapi = SmartlingFileApi(self.HOST, self.MY_API_KEY, self.MY_PROJECT_ID)
        self.fileProps = fileProps
        self.locale = locale

    def printMarker(self, caption):
        print "--" + caption + "-"*40

    def test(self):
        self.printMarker("file upload")
        print self.fapi.upload(self.fileProps.path, self.fileProps.name, self.fileProps.type)

        self.printMarker("files list")
        print self.fapi.list()

        self.printMarker("file status")
        print self.fapi.status(self.fileProps.name, self.locale)

        self.printMarker("file from server goes here")
        print self.fapi.get(self.fileProps.name, self.locale)
        

FILE_NAME      = "application.properties"
FILE_TYPE      = "JAVA_PROPERTIES"        
FILE_PATH      = "../resources/"

fileProps = FileProperties(FILE_PATH, FILE_NAME, FILE_TYPE)
example = SmartlingApiExample (fileProps, "ru-RU")
example.test()