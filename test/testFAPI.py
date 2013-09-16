''' Copyright 2012 Smartling, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this work except in compliance with the License.
 * You may obtain a copy of the License in the LICENSE file, or at:
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
'''

import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path) # allow to import ../smartlingApiSdk/SmartlingFileApi

from smartlingApiSdk.SmartlingFileApi import SmartlingFileApi
from smartlingApiSdk.UploadData import UploadData
from nose.tools import assert_equal

# don't forget to set real API_KEY and PROJECT_ID
# or use environment variables:
# export SL_API_KEY=********-****-****-****-************
# export SL_PROJECT_ID=*******    

class testFapi(object):
    HOST           = 'sandbox-api.smartling.com'
    MY_API_KEY     = "YOUR_API_KEY"
    MY_PROJECT_ID  = "YOUR_PROJECT_ID"
    
    FILE_NAME      = "java.properties"
    FILE_TYPE      = "javaProperties"        
    FILE_PATH      = "../resources/"
    FILE_NAME_NEW  = "java.properties.renamed"
    CALLBACK_URL   = "http://google.com/?q=hello"
    
    CODE_SUCCESS_TOKEN = '"code":"SUCCESS"'
    
    def setUp(self):
        self.MY_API_KEY    = os.environ.get('SL_API_KEY', self.MY_API_KEY)
        self.MY_PROJECT_ID = os.environ.get('SL_PROJECT_ID', self.MY_PROJECT_ID)
        self.fapi = SmartlingFileApi(self.HOST, self.MY_API_KEY, self.MY_PROJECT_ID)
        self.locale = "ru-RU"
        self.doUpload()
        
    def doUpload(self):
        #ensure file is uploaded which is necesary for all tests
        uploadData = UploadData(self.FILE_PATH, self.FILE_NAME, self.FILE_TYPE)
        uploadData.setCallbackUrl(self.CALLBACK_URL)
        return self.fapi.upload(uploadData)

    def testFileList(self):
        res, status = self.fapi.list()
        assert_equal(True, res.find(self.CODE_SUCCESS_TOKEN) > 0 )
        
    def testFileStatus(self):
        res, status = self.fapi.status(self.FILE_NAME, self.locale)
        assert_equal(True, res.find(self.CODE_SUCCESS_TOKEN) > 0 )

    def testGetFileFromServer(self):
        res, status = self.fapi.get(self.FILE_NAME, self.locale)
        lines = open( self.FILE_PATH + self.FILE_NAME, "rb" ).readlines()
        assert_equal( len(res.split("\n")), len(lines) )
        
    def testGetFileWithTypeFromServer(self):
        res, status = self.fapi.get(self.FILE_NAME, self.locale, retrievalType='pseudo')
        lines = open( self.FILE_PATH + self.FILE_NAME, "rb" ).readlines()
        assert_equal( len(res.split("\n")), len(lines) )    
        
    def testFileDelete(self):
        res, status = self.fapi.list()
        count_old = res.count('"fileUri":')
        res, status = self.fapi.delete(self.FILE_NAME)
        assert_equal(True, res.find(self.CODE_SUCCESS_TOKEN) > 0 )
        res, status = self.fapi.list()
        count_new = res.count('"fileUri":')
        assert_equal(count_old-1,count_new)
        self.doUpload() #ensure file is uploaded back after it's deleted

    def testFileRename(self):
        self.fapi.delete(self.FILE_NAME_NEW)
        res, status = self.fapi.rename(self.FILE_NAME, self.FILE_NAME_NEW)
        assert_equal(True, res.find(self.CODE_SUCCESS_TOKEN) > 0 )
