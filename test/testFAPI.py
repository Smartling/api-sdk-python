import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path) # allow to import ../apisdk/SmartlingFileApi

from apisdk.SmartlingFileApi import SmartlingFileApi
from nose.tools import assert_equal


class testFapi(object):
    HOST           = 'sandbox-api.smartling.com'
    MY_API_KEY     = "00212573-255a-4ced-87bc-005be5861d45"
    MY_PROJECT_ID  = "f4c6f2413"
    
    FILE_NAME      = "application.properties"
    FILE_TYPE      = "JAVA_PROPERTIES"        
    FILE_PATH      = "../resources/"
    
    CODE_SUCCESS_TOKEN = '"code":"SUCCESS"'
    
    def setUp(self):
        self.fapi = SmartlingFileApi(self.HOST, self.MY_API_KEY, self.MY_PROJECT_ID)
        self.locale = "ru-RU"

    def testUpload(self):
        res = self.fapi.upload(self.FILE_PATH, self.FILE_NAME, self.FILE_TYPE)
        assert_equal(True, res.find(self.CODE_SUCCESS_TOKEN) > 0 )

    def testFileList(self):
        res = self.fapi.list()
        assert_equal(True, res.find(self.CODE_SUCCESS_TOKEN) > 0 )
        
    def testFileStatus(self):
        res = self.fapi.status(self.FILE_NAME, self.locale)
        assert_equal(True, res.find(self.CODE_SUCCESS_TOKEN) > 0 )

    def testGetFileFromServer(self):
        res = self.fapi.get(self.FILE_NAME, self.locale)
        lines = open( self.FILE_PATH + self.FILE_NAME, "rb" ).readlines()
        assert_equal( len(res.split("\n")), len(lines) )