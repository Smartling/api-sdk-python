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

import os
import sys

lib_path = os.path.abspath('../')
sys.path.append(lib_path)  # allow to import ../smartlingApiSdk/SmartlingFileApi

from smartlingApiSdk.SmartlingFileApi import SmartlingFileApi
from smartlingApiSdk.UploadData import UploadData
from nose.tools import assert_equal

# don't forget to set real API_KEY and PROJECT_ID
# or use environment variables:
# export SL_API_KEY=********-****-****-****-************
# export SL_PROJECT_ID=*******
# export SL_LOCALE=**-**


class testFapi(object):
    MY_API_KEY = "YOUR_API_KEY"
    MY_PROJECT_ID = "YOUR_PROJECT_ID"
    SL_LOCALE = "ru-RU"

    FILE_PATH = "../resources/"
    CALLBACK_URL = "http://google.com/?q=hello"

    FILE_NAME = "test_import.xml"
    FILE_NAME_IMPORT = "test_import_es.xml"
    FILE_TYPE = "android"
    HOST = 'api.smartling.com'


    CODE_SUCCESS_TOKEN = 'SUCCESS'

    def setUp(self):
        self.MY_API_KEY = os.environ.get('SL_API_KEY', self.MY_API_KEY)
        self.MY_PROJECT_ID = os.environ.get('SL_PROJECT_ID', self.MY_PROJECT_ID)
        self.fapi = SmartlingFileApi(self.HOST, self.MY_API_KEY, self.MY_PROJECT_ID)
        self.locale =  os.environ.get('SL_LOCALE', self.SL_LOCALE)
        self.doUpload()

    def doUpload(self):
        #ensure file is uploaded which is necessary for all tests
        uploadData = UploadData(self.FILE_PATH, self.FILE_NAME, self.FILE_TYPE)
        uploadData.setCallbackUrl(self.CALLBACK_URL)
        return self.fapi.upload(uploadData)

    def tearDown(self):
        print self.fapi.delete(self.FILE_NAME)
        print "lits after delete"
        print self.fapi.list()
        
    def testImport(self):
        uploadData = UploadData(self.FILE_PATH, self.FILE_NAME, self.FILE_TYPE)
        uploadData.uri = uploadData.name
        uploadData.name = self.FILE_NAME_IMPORT
        resp, status = self.fapi.import_call(uploadData, self.locale, translationState="READY_FOR_PUBLISH")
        print resp
        assert_equal(resp.code, self.CODE_SUCCESS_TOKEN)
        assert_equal(resp.data.wordCount, 2)
        assert_equal(resp.data.stringCount, 2)
        assert_equal(resp.data.translationImportErrors, [])

