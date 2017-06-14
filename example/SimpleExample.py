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
from smartlingApiSdk.Credentials import Credentials

#File attributes to upload to Smartling server
FILE_TYPE = "javaProperties"
FILE_NAME = "java.properties"
FILE_PATH = "../resources/"

#set Smartling creadentials via helper Credentials class
credentials = Credentials() #Gets your Smartling credetnials from environment variables
MY_USER_IDENTIFIER = credentials.MY_USER_IDENTIFIER
MY_USER_SECRET = credentials.MY_USER_SECRET
MY_PROJECT_ID = credentials.MY_PROJECT_ID
MY_LOCALE = credentials.MY_LOCALE

#set proxy settigns if necessary
useProxy = False
if useProxy :
    proxySettings = ProxySettings("login", "password", "proxy_host", "proxy_port")
else:
    proxySettings = None

#initializa api object
fapi = SmartlingFileApiV2( MY_USER_IDENTIFIER, MY_USER_SECRET, MY_PROJECT_ID, proxySettings)
        
#Upload file to Smartling

print("\nUploading ...")
path = FILE_PATH + FILE_NAME

customFileUri = "/simple/test"
#parameter `fileUri` is optional, if not set - value of `path` is be used as fiel uri here and
#should be used in all requests that need file uri
#like fapi.status, fapi.get, fapi.delete
resp, code = fapi.upload(path, FILE_TYPE, fileUri=customFileUri, authorize=True)
print(resp, code)
if 200!=code:
    raise Exception("failed")

#List uploaded files
print("\nList ...")
resp, code = fapi.list()
print("items size= ", len(resp.data.items))
print(code, resp)

#check file status
print("\nFile status ...")
resp, code = fapi.status(customFileUri)
print(code, resp)
print(resp.data.fileUri)
print("items size=", len(resp.data.items))

#read uplaoded file
print("\nRead file from server ...")
resp, code = fapi.get(customFileUri, MY_LOCALE)
print(resp, code)

#delete file
print("\nDelete file ...")
resp, code = fapi.delete(customFileUri)
print(resp, code)
    
    
    
    
