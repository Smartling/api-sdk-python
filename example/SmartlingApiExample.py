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
lib_path = os.path.abspath('../')
sys.path.append(lib_path)  # allow to import ../smartlingApiSdk/SmartlingFileApi

from smartlingApiSdk.SmartlingFileApi import SmartlingFileApiFactory, ProxySettings
from smartlingApiSdk.SmartlingDirective import SmartlingDirective
from smartlingApiSdk.UploadData import UploadData


class SmartlingApiExample:

    MY_API_KEY = "YOUR_API_KEY" #should be changed with read values
    MY_PROJECT_ID = "YOUR_PROJECT_ID" #should be changed with real values

    def __init__(self, useSandbox, uploadData, locale, new_name):
        self.getCredentials()

        useProxy = False
        if useProxy :
            proxySettings = ProxySettings("login", "password", "proxy_host", "proxy_port")
        else:
            proxySettings = None

        if useSandbox:
            self.fapi = SmartlingFileApiFactory().getSmartlingTranslationApi(False, self.MY_API_KEY, self.MY_PROJECT_ID, proxySettings)
        else:
            self.fapi = SmartlingFileApiFactory().getSmartlingTranslationApiProd(self.MY_API_KEY, self.MY_PROJECT_ID, proxySettings)
        self.uploadData = uploadData
        self.locale = locale
        self.new_name = new_name
        
    def getCredentials(self):
        """ get api key and project id from environment variables
            to set environment variables use command : export SL_API_KEY=******* ; export SL_PROJECT_ID=****** """
        self.MY_API_KEY = os.environ.get('SL_API_KEY', self.MY_API_KEY)
        self.MY_PROJECT_ID = os.environ.get('SL_PROJECT_ID', self.MY_PROJECT_ID)


    def printMarker(self, caption):
        print "--" + caption + "-" * 40

    def test_import(self, name_to_import):
        """ this method tests `import` command """
        self.printMarker("file upload")
        #upload file first to be able upload it's translations later
        print self.fapi.upload(self.uploadData)

        self.printMarker("files list")
        #list all files to ensure upload worked
        print self.fapi.list()

        self.printMarker("importing uploaded")
        old_name = self.uploadData.name
        #set correct uri/name for file to be imported
        self.uploadData.uri = self.uploadData.name
        self.uploadData.name = name_to_import

        #import translations from file
        print self.fapi.import_call(self.uploadData, self.locale, translationState="READY_FOR_PUBLISH")

        self.uploadData.name = old_name

        #perform `last_modified` command
        self.printMarker("last modified")
        resp, code = self.fapi.last_modified(self.uploadData.name)
        print "resp.messages=", resp.messages
        print "resp.code=", resp.code
        print "resp.data.items="
        for v in resp.data.items: print v
        
        self.printMarker("delete from server goes here")
        #delete test file imported in the beginning of test
        print self.fapi.delete(self.uploadData.name)

    def test(self):
        """ simple illustration for set of API commands: upload, list, status, get, rename, delete """
        self.printMarker("file upload")
        print self.fapi.upload(self.uploadData)

        self.printMarker("files list")
        print self.fapi.list()

        self.printMarker("file status")
        print self.fapi.status(self.uploadData.name, self.locale)

        self.printMarker("file from server goes here")
        print self.fapi.get(self.uploadData.name, self.locale)

        self.printMarker("renaming file")
        print self.fapi.rename(self.uploadData.name, self.new_name)

        self.printMarker("delete from server goes here")
        print self.fapi.delete(self.new_name)

        self.printMarker("doing list again to see if it's deleted")
        print self.fapi.list()


FILE_NAME = "java.properties"
FILE_NAME_UTF16 = "javaUTF16.properties"
FILE_TYPE = "javaProperties"
FILE_PATH = "../resources/"
FILE_NAME_RENAMED = "java.properties.renamed"
CALLBACK_URL = "http://yourdomain.com/callback"


FILE_NAME_IMPORT = "test_import.xml"
FILE_NAME_TO_IMPORT = "test_import_es.xml"
FILE_TYPE_IMPORT ="android"

def ascii_test():
    #test simple file
    uploadDataASCII = UploadData(FILE_PATH, FILE_NAME, FILE_TYPE)
    uploadDataASCII.addDirective(SmartlingDirective("placeholder_format_custom", "\[.+?\]"))
    useSandbox = False
    example = SmartlingApiExample(useSandbox, uploadDataASCII, "it-IT", FILE_NAME_RENAMED)
    example.test()

def utf16_test():
    #add charset and approveContent parameters
    uploadDataUtf16 = UploadData(FILE_PATH, FILE_NAME_UTF16, FILE_TYPE)
    uploadDataUtf16.setApproveContent("true")
    uploadDataUtf16.setCallbackUrl(CALLBACK_URL)
    useSandbox = False
    example = SmartlingApiExample(useSandbox, uploadDataUtf16, "it-IT", FILE_NAME_RENAMED)
    example.test()

def import_test():
    #example for import and last_modified commands
    uploadDataImport = UploadData(FILE_PATH, FILE_NAME_IMPORT, FILE_TYPE_IMPORT)
    uploadDataImport.addDirective(SmartlingDirective("placeholder_format_custom", "\[.+?\]"))
    useSandbox = False
    example = SmartlingApiExample(useSandbox, uploadDataImport, "it-IT", FILE_NAME_RENAMED)
    example.test_import(FILE_NAME_TO_IMPORT)

ascii_test()
utf16_test()
import_test()
