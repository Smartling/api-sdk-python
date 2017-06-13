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

from smartlingApiSdk.SmartlingFileApiV2 import SmartlingFileApiV2
from smartlingApiSdk.ProxySettings import ProxySettings
from smartlingApiSdk.SmartlingDirective import SmartlingDirective
from smartlingApiSdk.Credentials import Credentials

class SmartlingApiExample:

    def __init__(self, file_name, file_type, new_name):
        credentials = Credentials() #Gets your Smartling credetnials from environment variables

        self.MY_USER_IDENTIFIER = credentials.MY_USER_IDENTIFIER
        self.MY_USER_SECRET = credentials.MY_USER_SECRET
        self.MY_PROJECT_ID = credentials.MY_PROJECT_ID
        self.MY_LOCALE = credentials.MY_LOCALE

        useProxy = False
        if useProxy :
            proxySettings = ProxySettings("login", "password", "proxy_host", "proxy_port")
        else:
            proxySettings = None

        self.fapi = SmartlingFileApiV2( self.MY_USER_IDENTIFIER, self.MY_USER_SECRET, self.MY_PROJECT_ID, proxySettings)
        self.file_type = file_type
        self.file_name = file_name
        self.new_name = new_name
        
    def printMarker(self, caption):
        print("--" + caption + "-" * 40)

    def test_import(self, name_to_import):
        """ this method tests `import` command """
        self.printMarker("file upload")
        #upload file first to be able upload it's translations later
        
        path = FILE_PATH + self.file_name
        resp, code = self.fapi.upload(path, self.file_type)
        if 200!=code:
            raise Exception("failed")
   
        print(resp, code)
    
        self.printMarker("files list")
        #list all files to ensure upload worked
        resp, code = self.fapi.list()
        print(resp, code)

        self.printMarker("importing uploaded")
        #set correct uri/name for file to be imported
        path_to_import = FILE_PATH + name_to_import

        #import translations from file
        resp, code = self.fapi.import_call(path, path_to_import, 
                    self.file_type, self.MY_LOCALE, 
                     translationState="PUBLISHED")
        print(resp, code)

        if 200!=code:
            raise Exception("failed")

        #perform `last_modified` command
        self.printMarker("last modified")
        resp, code = self.fapi.last_modified(path, self.MY_LOCALE)
        print(resp, code)
        
        self.printMarker("delete from server goes here")
        #delete test file imported in the beginning of test
        resp, code = self.fapi.delete(path)
        print(resp, code)

    def test(self):
        """ simple illustration for set of API commands: upload, list, status, get, rename, delete """
        self.printMarker("file upload")
        path = FILE_PATH + self.file_name
        directives={"placeholder_format_custom" : "\[.+?\]"}
        resp, code = self.fapi.upload(path, self.file_type, authorize="true", callbackUrl=CALLBACK_URL, directives=directives)
        print(resp, code)
        if 200!=code:
            raise Exception("failed")

        self.printMarker("files list")
        resp, code = self.fapi.list()
        print(resp, code)

        self.printMarker("file status")
        resp, code = self.fapi.status(path)
        print(resp, code)

        self.printMarker("file from server goes here")
        resp, code = self.fapi.get(path, self.MY_LOCALE)
        print(resp, code)

        self.printMarker("renaming file")
        resp, code = self.fapi.rename(path, self.new_name)
        print(resp, code)

        self.printMarker("delete from server goes here")
        resp, code = self.fapi.delete(self.new_name)
        print(resp, code)

        self.printMarker("doing list again to see if it's deleted")
        resp, code = self.fapi.list()
        print(resp, code)


FILE_NAME = "java.properties"
FILE_NAME_UTF16 = "javaUTF16.properties"
FILE_TYPE = "javaProperties"
FILE_PATH = "../resources/"
FILE_NAME_RENAMED = "java.properties.renamed"
CALLBACK_URL = "http://yourdomain.com/callback"


FILE_NAME_IMPORT = "test_import.xml"
FILE_NAME_TO_IMPORT = "test_import_es.xml"
FILE_TYPE_IMPORT ="android"

def upload_test():
    #test simple file
    example = SmartlingApiExample(FILE_NAME, FILE_TYPE, FILE_NAME_RENAMED)
    example.test()

def import_test():
    #example for import and last_modified commands
    example = SmartlingApiExample(FILE_NAME_IMPORT, FILE_TYPE_IMPORT, FILE_NAME_RENAMED)
    example.test_import(FILE_NAME_TO_IMPORT)

upload_test()
import_test()
