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

from smartlingApiSdk.SmartlingFileApi import SmartlingFileApi, SmartlingFileApiFactory
from smartlingApiSdk.SmartlingDirective import SmartlingDirective
from smartlingApiSdk.UploadData import UploadData


class SmartlingApiExample:
    
    MY_API_KEY     = "YOUR_API_KEY"
    MY_PROJECT_ID  = "YOUR_PROJECT_ID"
    
    def __init__(self, useSandbox, uploadData, locale, new_name):
        if useSandbox :
            self.fapi = SmartlingFileApiFactory().getSmartlingTranslationApi(False, self.MY_API_KEY, self.MY_PROJECT_ID)
        else:
            self.fapi = SmartlingFileApiFactory().getSmartlingTranslationApiProd(self.MY_API_KEY, self.MY_PROJECT_ID)
        self.uploadData = uploadData
        self.locale = locale
        self.new_name = new_name

    def printMarker(self, caption):
        print "--" + caption + "-"*40

    def test(self):
        self.printMarker("file upload")
        print self.fapi.upload(self.uploadData)

        self.printMarker("files list")
        print self.fapi.list()

        self.printMarker("file status")
        print self.fapi.status(self.uploadData.name, self.locale)

        self.printMarker("file from server goes here")
        print self.fapi.get( self.uploadData.name, self.locale)
        
        self.printMarker("renaming file")
        print self.fapi.rename(self.uploadData.name, self.new_name)
        
        self.printMarker("delete from server goes here")
        print self.fapi.delete(self.new_name)
        
        self.printMarker("doing list again to see if it's deleted")
        print self.fapi.list()
        


FILE_NAME      = "java.properties"
FILE_NAME_UTF16= "javaUTF16.properties"
FILE_TYPE      = "javaProperties"        
FILE_PATH      = "../resources/"
FILE_NAME_RENAMED = "java.properties.renamed"
CALLBACK_URL      = "http://yourdomain.com/callback"

#test simple file
uploadDataASCII = UploadData(FILE_PATH, FILE_NAME, FILE_TYPE)
uploadDataASCII.addDirective(SmartlingDirective("placeholder_format_custom","\[.+?\]"))
useSandbox = False
example = SmartlingApiExample (useSandbox, uploadDataASCII, "ru-RU", FILE_NAME_RENAMED)
example.test()

#add charset and approveContent parameters
uploadDataUtf16 = UploadData(FILE_PATH, FILE_NAME_UTF16, FILE_TYPE)
uploadDataUtf16.setApproveContent("true")
uploadDataUtf16.setCallbackUrl(CALLBACK_URL)
useSandbox = True
example = SmartlingApiExample (useSandbox, uploadDataUtf16, "ru-RU", FILE_NAME_RENAMED)
example.test()
