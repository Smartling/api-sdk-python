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
sys.path.append(lib_path) # allow to import ../apisdk/SmartlingFileApi

from apisdk.SmartlingFileApi import SmartlingFileApi
from apisdk.UploadData import UploadData
from nose.tools import assert_equal


class testFapi(object):
    HOST           = 'sandbox-api.smartling.com'
    MY_API_KEY     = "YOUR_API_KEY"
    MY_PROJECT_ID  = "YOUR_PROJECT_ID"
    
    FILE_NAME      = "java.properties"
    FILE_TYPE      = "javaProperties"        
    FILE_PATH      = "../resources/"
    
    CODE_SUCCESS_TOKEN = '"code":"SUCCESS"'
    
    def setUp(self):
        self.fapi = SmartlingFileApi(self.HOST, self.MY_API_KEY, self.MY_PROJECT_ID)
        self.locale = "ru-RU"

    def testUpload(self):
        uploadData = UploadData(self.FILE_PATH, self.FILE_NAME, self.FILE_TYPE)
        res = self.fapi.upload(uploadData)
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