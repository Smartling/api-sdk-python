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
import zipfile
import StringIO
from datetime import date

lib_path = os.path.abspath('../')
sys.path.append(lib_path)  # allow to import ../smartlingApiSdk/SmartlingFileApi

from smartlingApiSdk.SmartlingFileApiV2 import SmartlingFileApiV2
from smartlingApiSdk.ProxySettings import ProxySettings
from nose.tools import assert_equal
from smartlingApiSdk.version import version
from smartlingApiSdk.Credentials import Credentials
from smartlingApiSdk.Constants import FileTypes

class testFapiV2(object):

    FILE_NAME = "java.properties"
    FILE_NAME_16 = "javaUTF16.properties"
    FILE_TYPE = "javaProperties"
    FILE_TYPE_CSV = "csv"
    FILE_PATH = "../resources/"
    FILE_NAME_NEW = "java.properties.renamed"
    FILE_NAME_NEW_16 = "javaUTF16.properties.renamed"
    FILE_NAME_CSV = "test.csv"
    
    FILE_NAME_IMPORT_ORIG = "test_import.xml"
    FILE_NAME_IMPORT_TRANSLATED = "test_import_es.xml"
    FILE_TYPE_IMPORT = "android"

    CALLBACK_URL = "http://google.com/?q=hello"

    CODE_SUCCESS_TOKEN = 'SUCCESS'
            

    def setUp(self):
        credentials = Credentials() #Gets your Smartling credetnials from environment variables
        self.MY_USER_IDENTIFIER = credentials.MY_USER_IDENTIFIER
        self.MY_USER_SECRET = credentials.MY_USER_SECRET
        self.MY_PROJECT_ID = credentials.MY_PROJECT_ID
        self.MY_LOCALE = credentials.MY_LOCALE
        
        #needed for testProjects
        self.MY_ACCOUNT_UID = credentials.MY_ACCOUNT_UID
    
        useProxy = False
        if useProxy :
            proxySettings = ProxySettings("login", "password", "proxy_host", "proxy_port or None")
        else:
            proxySettings = None        
        self.fapi = SmartlingFileApiV2(self.MY_USER_IDENTIFIER, self.MY_USER_SECRET, self.MY_PROJECT_ID, proxySettings)
        unique_suffix = "_" + version + "_" + `time.time()`
        self.uri = self.FILE_NAME + unique_suffix 
        self.doUpload(self.FILE_NAME, self.uri, self.FILE_TYPE)
        
        self.uri_csv = self.FILE_NAME_CSV + unique_suffix

        self.uri16 = self.FILE_NAME_16 + unique_suffix 
        self.doUpload(self.FILE_NAME_16, self.uri16, self.FILE_TYPE)
        
        self.uri_to_rename = self.FILE_NAME_NEW + unique_suffix
        self.uri_import = self.FILE_NAME_IMPORT_ORIG + unique_suffix
        
        print "setUp", "OK", "\n\n\n"


    def tearDown(self):
        res, status = self.fapi.delete(self.uri)
        assert_equal(200, status)
        assert_equal(self.CODE_SUCCESS_TOKEN, res.code)
        
        res, status = self.fapi.delete(self.uri16)
        assert_equal(200, status)
        assert_equal(self.CODE_SUCCESS_TOKEN, res.code)
        
        print "tearDown", "OK"

    def doUpload(self, name, uri, type):
        #ensure file is uploaded which is necessary for all tests
        uniqueUriForUploadTestFile = uri
        localeIdsToAuthorize = [self.MY_LOCALE]
        res, status = self.fapi.upload(self.FILE_PATH + name, type, fileUri = uniqueUriForUploadTestFile, localeIdsToAuthorize = localeIdsToAuthorize )
        
        assert_equal(200, status)
        assert_equal(self.CODE_SUCCESS_TOKEN, res.code)
        print status, res
        return res, status
        
    def testFileList(self):
        res, status = self.fapi.list(fileTypes=[FileTypes.android, FileTypes.javaProperties])
        assert_equal(self.CODE_SUCCESS_TOKEN, res.code)

        uris = map(lambda x:x['fileUri'], res.data.items)

        assert_equal(True, self.uri in uris)
        assert_equal(True, self.uri16 in uris)
        
        print "testFileList", "OK"

    def testFileListTypes(self):
        res, status = self.fapi.list_file_types()
        assert_equal(self.CODE_SUCCESS_TOKEN, res.code)
        print "testFileListTypes", "OK"
        
    def testGet(self):
        res, status = self.fapi.get(self.uri, self.MY_LOCALE)
        assert_equal(200, status)
        
        resp_lines_count = len(res.split("\n"))
        file_lines_count = len( open(self.FILE_PATH + self.FILE_NAME, "rb").readlines() )
        assert_equal(resp_lines_count, file_lines_count)
        
        print "testGet", "OK"
    
        res, status = self.fapi.get(self.uri16, self.MY_LOCALE)
        assert_equal(200, status)

        resp_lines_count = len(res.split("\n"))
        file_lines_count = len( open(self.FILE_PATH + self.FILE_NAME_16, "rb").readlines() )
        assert_equal(resp_lines_count, file_lines_count)
        print "testGet Utf16", "OK"
        
        
    def testGetMultipleLocalesAsZip(self):
        res, status = self.fapi.get_multiple_locales([self.uri,self.uri16], [self.MY_LOCALE])
        assert_equal(200, status)
        
        zfile = zipfile.ZipFile(StringIO.StringIO(res))
        names = zfile.namelist()
        
        assert_equal(True, self.MY_LOCALE+"/"+self.uri in names)
        assert_equal(True, self.MY_LOCALE+"/"+self.uri16 in names)
        
        print "testGetMultipleLocalesAsZip", "OK"


    def testGetAllLocalesZip(self):
        res, status = self.fapi.get_all_locales(self.uri)
        assert_equal(200, status)
        
        zfile = zipfile.ZipFile(StringIO.StringIO(res))
        names = zfile.namelist()
        
        assert_equal(True, self.MY_LOCALE+"/"+self.uri in names)
        
        print "testGetAllLocalesZip", "OK"


    def testGetOriginal(self):
        res, status = self.fapi.get_original(self.uri)
        assert_equal(200, status)
        
        orig = open(self.FILE_PATH + self.FILE_NAME, "r").read()
        assert_equal(res, orig)
        
        print "testGetOriginal", "OK"
    
        res, status = self.fapi.get_original(self.uri16)
        assert_equal(200, status)

        resp_lines_count = len(res.split("\n"))
        file_lines_count = len( open(self.FILE_PATH + self.FILE_NAME_16, "rb").readlines() )
        assert_equal(resp_lines_count, file_lines_count)
        print "testGetOriginal Utf16", "OK"        


    def testGetAllLocalesCsv(self):
        self.doUpload(self.FILE_NAME_CSV, self.uri_csv, self.FILE_TYPE_CSV)
        res, status = self.fapi.get_all_locales_csv(self.uri_csv)
        assert_equal(200, status)

        res, status = self.fapi.delete(self.uri_csv)
        assert_equal(200, status)
        assert_equal(self.CODE_SUCCESS_TOKEN, res.code)
        print "testGetAllLocalesCsv", "OK"

    def testProjects(self):
        if self.MY_ACCOUNT_UID == "CHANGE_ME":
            print "can't test projects api call, set self.MY_ACCOUNT_UID or export SL_ACCOUNT_UID=*********"
            return
        res, status = self.fapi.projects(self.MY_ACCOUNT_UID)
        
        assert_equal(200, status)
        assert_equal(self.CODE_SUCCESS_TOKEN, res.code)
        
        projects = map(lambda x:x['projectId'], res.data.items)

        assert_equal(True, self.MY_PROJECT_ID in projects)
        print "testProjects", "OK"

    def testProjectDetails(self):
        res, status = self.fapi.project_details()
        
        assert_equal(200, status)
        assert_equal(self.CODE_SUCCESS_TOKEN, res.code)
        assert_equal(self.MY_PROJECT_ID, res.data.projectId)
        
        print "testProjectDetails", "OK"

    def testStatus(self):
        res, status = self.fapi.status(self.uri)
        
        assert_equal(200, status)
        assert_equal(self.CODE_SUCCESS_TOKEN, res.code)
        assert_equal(res.data.fileUri, self.uri)
        assert_equal(True, len(res.data.items) > 0)
        
        print "testStatus", "OK"


    def testStatusLocale(self):
        res, status = self.fapi.status_locale(self.uri, self.MY_LOCALE)
        
        assert_equal(200, status)
        assert_equal(self.CODE_SUCCESS_TOKEN, res.code)
        assert_equal(res.data.fileUri, self.uri)
        assert_equal(res.data.fileType, self.FILE_TYPE)
        
        print "testStatusLocale", "OK"

    def testFileRename(self):
    
        res, status = self.fapi.rename(self.uri, self.uri_to_rename)
        assert_equal(200, status)
        assert_equal(self.CODE_SUCCESS_TOKEN, res.code)
        
        #rename it back so tearDown could remove it
        res, status = self.fapi.rename(self.uri_to_rename, self.uri)
        assert_equal(200, status)
        assert_equal(self.CODE_SUCCESS_TOKEN, res.code)
        
        print "testStatusLocale", "OK"
         
    def testLastModified(self):
        resp, status = self.fapi.last_modified(self.uri, self.MY_LOCALE)
        assert_equal(200, status)
        assert_equal(self.CODE_SUCCESS_TOKEN, resp.code)

        lm_date = resp.data.lastModified[:10]
        assert_equal(lm_date,  date.today().isoformat())

        resp, status = self.fapi.last_modified(self.uri16, self.MY_LOCALE)
        assert_equal(200, status)
        assert_equal(self.CODE_SUCCESS_TOKEN, resp.code)

        lm_date = resp.data.lastModified[:10]
        assert_equal(lm_date,  date.today().isoformat())

        print "testLastModified", "OK"
        
    def testLastModifiedAll(self):
        resp, status = self.fapi.last_modified_all(self.uri)
        assert_equal(200, status)
        assert_equal(self.CODE_SUCCESS_TOKEN, resp.code)
        assert_equal(True, resp.data.items > 0)

        resp, status = self.fapi.last_modified_all(self.uri16)
        assert_equal(200, status)
        assert_equal(self.CODE_SUCCESS_TOKEN, resp.code)
        assert_equal(True, resp.data.items > 0)

        print "testLastModifiedAll", "OK"        
        
    def testImport(self):
        res, status = self.fapi.upload(self.FILE_PATH + self.FILE_NAME_IMPORT_ORIG, self.FILE_TYPE_IMPORT , fileUri=self.uri_import)

        assert_equal(200, status)
        assert_equal(self.CODE_SUCCESS_TOKEN, res.code)
        
        originalPath = self.FILE_PATH + self.FILE_NAME_IMPORT_ORIG
        translatedPath = self.FILE_PATH + self.FILE_NAME_IMPORT_TRANSLATED
    
        resp, status = self.fapi.import_call(originalPath, translatedPath, 
            self.FILE_TYPE_IMPORT, self.MY_LOCALE, 
            fileUri=self.uri_import, translationState="PUBLISHED")
            
        assert_equal(resp.code, self.CODE_SUCCESS_TOKEN)
        assert_equal(resp.data.wordCount, 2)
        assert_equal(resp.data.stringCount, 2)
        assert_equal(resp.data.translationImportErrors, [])

        res, status = self.fapi.delete(self.uri_import)
        assert_equal(200, status)
        assert_equal(self.CODE_SUCCESS_TOKEN, res.code)

        print "testImport", "OK"  
        
    def testListAuthorizedLocales(self):
        resp, status = self.fapi.last_modified_all(self.uri)
        assert_equal(200, status)
        assert_equal(self.CODE_SUCCESS_TOKEN, resp.code)
        assert_equal(True, resp.data.items > 0)

        locales = map(lambda x:x['localeId'], resp.data.items)
        assert_equal(True, self.MY_LOCALE in locales)
        print "testListAuthorizedLocales", "OK" 
    
    
    def testAuthorize(self):
        res, status = self.fapi.authorize(self.uri, [self.MY_LOCALE, 'uk-UA'])
        assert_equal(200, status)
        assert_equal(self.CODE_SUCCESS_TOKEN, res.code)
        
        print "testAuthorize", "OK" 
        
    def testUnauthorize(self):
        res, status = self.fapi.unauthorize(self.uri, [self.MY_LOCALE, 'uk-UA'])
        assert_equal(200, status)
        assert_equal(self.CODE_SUCCESS_TOKEN, res.code)
        
        print "testUnauthorize", "OK" 
        

    def testGetTranslations(self):        
        res, status = self.fapi.get_translations(self.uri, self.FILE_PATH+self.FILE_NAME, (self.MY_LOCALE))
        
        assert_equal(200, status)
        
        resp_lines_count = len(res.split("\n"))
        file_lines_count = len( open(self.FILE_PATH + self.FILE_NAME, "rb").readlines() )
        assert_equal(resp_lines_count, file_lines_count)
        
        print "testUnauthorize", "OK" 
        