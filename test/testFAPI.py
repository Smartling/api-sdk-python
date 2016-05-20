#!/usr/bin/python
# -*- coding: utf-8 -*-


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
import time

lib_path = os.path.abspath('../')
sys.path.append(lib_path)  # allow to import ../smartlingApiSdk/SmartlingFileApi

from smartlingApiSdk.SmartlingFileApi import SmartlingFileApi, SmartlingFileApiFactory
from smartlingApiSdk.ProxySettings import ProxySettings
from smartlingApiSdk.UploadData import UploadData
from nose.tools import assert_equal

noKeymessage = """ don't forget to set real API_KEY and PROJECT_ID
 or use environment variables:
 export SL_API_KEY=********-****-****-****-************
 export SL_PROJECT_ID=*******
"""

class testFapi(object):
    MY_API_KEY = "YOUR_API_KEY"
    MY_PROJECT_ID = "YOUR_PROJECT_ID"

    FILE_NAME = "java.properties"
    FILE_NAME_16 = "javaUTF16.properties"
    FILE_TYPE = "javaProperties"
    FILE_PATH = "../resources/"
    FILE_NAME_NEW = "java.properties.renamed"
    FILE_NAME_NEW_16 = "javaUTF16.properties.renamed"

    CALLBACK_URL = "http://google.com/?q=hello"

    CODE_SUCCESS_TOKEN = '"code":"SUCCESS"'

    def setUp(self):
        self.MY_API_KEY = os.environ.get('SL_API_KEY', self.MY_API_KEY)
        self.MY_PROJECT_ID = os.environ.get('SL_PROJECT_ID', self.MY_PROJECT_ID)
        if self.MY_PROJECT_ID == "YOUR_PROJECT_ID":
            raise noKeymessage 
        
        useProxy = False
        if useProxy :
            proxySettings = ProxySettings("login", "password", "proxy_host", "proxy_port or None")
        else:
            proxySettings = None        
        self.fapi = SmartlingFileApiFactory().getSmartlingTranslationApi(self.MY_API_KEY, self.MY_PROJECT_ID, proxySettings)
        self.locale =  os.environ.get('SL_LOCALE', "ru-RU")
        timestamp = `time.time()`
        self.uri = self.FILE_NAME + timestamp 
        self.doUpload(self.FILE_NAME, self.uri)

        self.uri16 = self.FILE_NAME_16 + timestamp 
        self.doUpload(self.FILE_NAME_16, self.uri16)


    def tearDown(self):
        res, status = self.fapi.delete(self.uri)
        res, status = self.fapi.delete(self.uri16)

    def doUpload(self, name, uri):
        #ensure file is uploaded which is necessary for all tests
        uploadData = UploadData(self.FILE_PATH, name, self.FILE_TYPE)
        uploadData.setUri(uri)
        uploadData.setCallbackUrl(self.CALLBACK_URL)
        return self.fapi.upload(uploadData)

    def testFileList(self):
        res, status = self.fapi.list()
        assert_equal(True, res.find(self.CODE_SUCCESS_TOKEN) > 0)

    def testFileStatus(self):
        res, status = self.fapi.status(self.uri, self.locale)
        assert_equal(True, res.find(self.CODE_SUCCESS_TOKEN) > 0)
        
        res, status = self.fapi.status(self.uri16, self.locale)
        assert_equal(True, res.find(self.CODE_SUCCESS_TOKEN) > 0)

    def testGetFileFromServer(self):
        res, status = self.fapi.get(self.uri, self.locale)
        lines = open(self.FILE_PATH + self.FILE_NAME, "rb").readlines()
        assert_equal(len(res.split("\n")), len(lines))

        res, status = self.fapi.get(self.uri16, self.locale)
        lines = open(self.FILE_PATH + self.FILE_NAME_16, "rb").readlines()
        assert_equal(len(res.split("\n")), len(lines))
        
    def testGetFileWithTypeFromServer(self):
        res, status = self.fapi.get(self.uri, self.locale, retrievalType='pseudo')
        lines = open(self.FILE_PATH + self.FILE_NAME, "rb").readlines()
        assert_equal(len(res.split("\n")), len(lines))
        
        res, status = self.fapi.get(self.uri16, self.locale, retrievalType='pseudo')
        lines = open(self.FILE_PATH + self.FILE_NAME_16, "rb").readlines()
        assert_equal(len(res.split("\n")), len(lines))

    def testFileDelete(self):
        res, status = self.fapi.list(uriMask="*"+self.uri)
        count_old = res.count('"fileUri":')
        res, status = self.fapi.delete(self.uri)
        assert_equal(True, res.find(self.CODE_SUCCESS_TOKEN) > 0)
        
        res, status = self.fapi.delete(self.uri16)
        assert_equal(True, res.find(self.CODE_SUCCESS_TOKEN) > 0)
 
    def testFileRename(self):
        res, status = self.fapi.rename(self.uri, self.FILE_NAME_NEW)
        assert_equal(True, res.find(self.CODE_SUCCESS_TOKEN) > 0)
        
        res, status = self.fapi.rename(self.FILE_NAME_NEW, self.uri)
        assert_equal(True, res.find(self.CODE_SUCCESS_TOKEN) > 0) 
        
    def testLastModified(self):
        resp, status = self.fapi.last_modified(self.uri)
        assert_equal(True, resp.find(self.CODE_SUCCESS_TOKEN) > 0)
        assert_equal(True, len(resp.data.items)>0)

        resp, status = self.fapi.last_modified(self.uri16)
        assert_equal(True, resp.find(self.CODE_SUCCESS_TOKEN) > 0)
        assert_equal(True, len(resp.data.items)>0)

